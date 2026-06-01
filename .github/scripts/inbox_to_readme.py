#!/usr/bin/env python3
"""Inbox -> README automation.

Batch-processes open Issues labeled `inbox`: extract GitHub repo URLs, dedup
against README.md, fetch repo metadata, ask GitHub Models to pick a category,
insert formatted entries, commit to main, then close/relabel the Issues.

Spec: openspec/changes/inbox-to-readme/ (archived under openspec/changes/archive/).

Deterministic work (extract, dedup, fetch, format, insert, commit) lives here;
the model does exactly one thing: pick an existing category or flag "none fits".
No external API key — GitHub Models is reached with the built-in GITHUB_TOKEN.
"""
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

REPO = os.environ["GITHUB_REPOSITORY"]           # "owner/repo"
TOKEN = os.environ["GITHUB_TOKEN"]
README = "README.md"

INBOX_LABEL = "inbox"
DONE_LABEL = "done"
NEEDS_LABEL = "needs-category"

BATCH_SIZE = 20                                  # net-new tools per model request
MODEL = "openai/gpt-4o"                          # tunable; any GitHub Models id
GH_API = "https://api.github.com"
MODELS_API = "https://models.github.ai/inference/chat/completions"

# First two path segments of a github.com URL. Reserved/non-repo owners (e.g.
# github.com/features) are filtered later by the 404 from the metadata fetch.
REPO_URL_RE = re.compile(r"https?://github\.com/([A-Za-z0-9._-]+)/([A-Za-z0-9._-]+)")
TOC_HEADING = "目錄"                              # the table-of-contents, not a category


# --------------------------------------------------------------------------- #
# HTTP helpers
# --------------------------------------------------------------------------- #
def _request(url, *, method="GET", headers=None, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode()
    except urllib.error.HTTPError as exc:
        # Surface GitHub's error body (the real reason) but keep the HTTPError
        # type so callers can still branch on exc.code (e.g. 404 metadata).
        detail = exc.read().decode(errors="replace")
        sys.stderr.write(f"{method} {url} -> HTTP {exc.code}: {detail[:500]}\n")
        raise
    return json.loads(body) if body else None


def gh_api(path, *, method="GET", payload=None):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }
    return _request(f"{GH_API}{path}", method=method, headers=headers, payload=payload)


def models_chat(messages):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {"model": MODEL, "messages": messages, "temperature": 0}
    resp = _request(MODELS_API, method="POST", headers=headers, payload=payload)
    if not resp or not resp.get("choices"):
        raise ValueError(f"unexpected Models response: {resp}")
    return resp["choices"][0]["message"]["content"]


# --------------------------------------------------------------------------- #
# Collection & dedup
# --------------------------------------------------------------------------- #
def normalize_repo(owner, repo):
    repo = repo[:-4] if repo.endswith(".git") else repo
    return owner, repo


def canonical_url(owner, repo):
    return f"https://github.com/{owner}/{repo}"


def list_inbox_issues():
    label = urllib.parse.quote(INBOX_LABEL, safe="")
    issues, page = [], 1
    while True:
        batch = gh_api(
            f"/repos/{REPO}/issues?state=open&labels={label}&per_page=100&page={page}"
        )
        issues.extend(batch)
        if len(batch) < 100:        # last page reached
            break
        page += 1
    # /issues also returns PRs; drop them.
    return [i for i in issues if "pull_request" not in i]


def extract_repos(body):
    """Return ordered unique (owner, repo) tuples found in an Issue body."""
    seen, out = set(), []
    for owner, repo in REPO_URL_RE.findall(body or ""):
        owner, repo = normalize_repo(owner, repo)
        key = (owner.lower(), repo.lower())
        if key not in seen:
            seen.add(key)
            out.append((owner, repo))
    return out


def readme_existing_urls(text):
    return {f"{o.lower()}/{r.lower()}" for o, r in
            (normalize_repo(o, r) for o, r in REPO_URL_RE.findall(text))}


def readme_categories(text):
    """Category headings, excluding the table-of-contents heading."""
    return [h for h in re.findall(r"^## (.+)$", text, re.MULTILINE)
            if h.strip() != TOC_HEADING]


# --------------------------------------------------------------------------- #
# Metadata & formatting
# --------------------------------------------------------------------------- #
def fetch_metadata(owner, repo):
    """Return dict(name, description, language) or None if the repo is gone."""
    try:
        data = gh_api(f"/repos/{owner}/{repo}")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise
    return {
        "name": data["name"],
        "description": (data.get("description") or "").strip(),
        "language": data.get("language"),
    }


def format_entry(meta, url):
    desc = meta["description"] or "No description"
    if desc[-1] not in ".!?":
        desc += "."
    lang = f" `{meta['language']}`" if meta["language"] else ""
    return f"- **{meta['name']}** — {desc}{lang}\n  <br/>{url}"


# --------------------------------------------------------------------------- #
# Categorization (the only model-driven step)
# --------------------------------------------------------------------------- #
def categorize(tools, categories):
    """tools: list of dict(url, name, description). Returns {url: result}.

    result is {"category": <heading>} or {"new_category": {name, macro_section}}.
    Raises on malformed output or an unknown, non-flagged category (fail-closed).
    """
    results = {}
    for start in range(0, len(tools), BATCH_SIZE):
        chunk = tools[start:start + BATCH_SIZE]
        results.update(_categorize_chunk(chunk, categories))
    return results


def _categorize_chunk(chunk, categories):
    cat_list = "\n".join(f"- {c}" for c in categories)
    tool_list = "\n".join(
        f'{i}. {t["name"]} — {t["description"]}  ({t["url"]})'
        for i, t in enumerate(chunk)
    )
    system = (
        "You sort AI/dev tools into a curated README. Categories are organized by "
        "an agent-workflow function (where the tool sits in an agent's workflow), "
        "not by form factor. Pick the single best-fitting EXISTING category for each "
        "tool. Only if none reasonably fits, propose a new category instead."
    )
    user = (
        f"EXISTING CATEGORIES (use the heading text verbatim):\n{cat_list}\n\n"
        f"TOOLS:\n{tool_list}\n\n"
        "Reply with ONLY a JSON array, one object per tool in order:\n"
        '{"url": "<url>", "category": "<exact existing heading>"} if one fits, OR\n'
        '{"url": "<url>", "category": null, '
        '"new_category": {"name": "<short heading>", "macro_section": "<which group>"}} '
        "if none fits. No prose, no code fences."
    )
    raw = models_chat([
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ])
    parsed = _parse_json_array(raw)
    valid = set(categories)
    by_url = {}
    for obj in parsed:
        url = obj["url"]
        cat = obj.get("category")
        if cat is None:
            new = obj.get("new_category")
            if not new or "name" not in new:
                raise ValueError(f"null category without a new_category for {url}")
            by_url[url] = {"new_category": new}
        elif cat in valid:
            by_url[url] = {"category": cat}
        else:
            # Hallucinated heading, not flagged as a suggestion -> fail the run.
            raise ValueError(f"model returned unknown category {cat!r} for {url}")
    missing = {t["url"] for t in chunk} - by_url.keys()
    if missing:
        raise ValueError(f"model omitted results for: {missing}")
    return by_url


def _parse_json_array(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw[raw.index("\n") + 1:] if "\n" in raw else raw
    start, end = raw.find("["), raw.rfind("]")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON array in model reply: {raw[:200]!r}")
    return json.loads(raw[start:end + 1])


# --------------------------------------------------------------------------- #
# README insertion
# --------------------------------------------------------------------------- #
def insert_entries(text, entries_by_category):
    """entries_by_category: {heading: [entry, ...]}. Returns new README text."""
    lines = text.split("\n")
    headings = {}
    for idx, line in enumerate(lines):
        m = re.match(r"^## (.+)$", line)
        if m:
            headings[m.group(1).strip()] = idx

    # Insert from the bottom up so earlier indices stay valid.
    for heading in sorted(entries_by_category, key=lambda h: headings[h], reverse=True):
        start = headings[heading]
        end = _section_end(lines, start)
        insert_at = end
        while insert_at > start + 1 and lines[insert_at - 1].strip() == "":
            insert_at -= 1
        lines[insert_at:insert_at] = entries_by_category[heading]
    return "\n".join(lines)


def _section_end(lines, start):
    for idx in range(start + 1, len(lines)):
        if re.match(r"^## ", lines[idx]):
            return idx
    return len(lines)


# --------------------------------------------------------------------------- #
# Git
# --------------------------------------------------------------------------- #
def git_commit(added):
    subprocess.run(["git", "add", README], check=True)
    summary = ", ".join(added)
    body = "\n".join(f"- {name}" for name in added)
    message = f"docs: add {len(added)} tool(s) from inbox — {summary}\n\n{body}"
    subprocess.run(["git", "commit", "-m", message], check=True)
    # Rebase onto any concurrent push to main before pushing (requires full
    # history — the workflow checks out with fetch-depth: 0).
    subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
    subprocess.run(["git", "push"], check=True)


# --------------------------------------------------------------------------- #
# Issue lifecycle
# --------------------------------------------------------------------------- #
def comment(number, text):
    gh_api(f"/repos/{REPO}/issues/{number}/comments", method="POST", payload={"body": text})


def relabel(number, remove, add):
    try:
        seg = urllib.parse.quote(remove, safe="")
        gh_api(f"/repos/{REPO}/issues/{number}/labels/{seg}", method="DELETE")
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
    gh_api(f"/repos/{REPO}/issues/{number}/labels", method="POST", payload={"labels": [add]})


def close_issue(number):
    gh_api(f"/repos/{REPO}/issues/{number}", method="PATCH", payload={"state": "closed"})


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    readme = open(README, encoding="utf-8").read()
    existing = readme_existing_urls(readme)
    categories = readme_categories(readme)

    issues = list_inbox_issues()
    if not issues:
        print("No inbox issues. Nothing to do.")
        return

    # Per-issue candidate repos and the set seen so far this run (intra-batch dedup).
    batch_seen = set()
    issue_repos = {}        # number -> list of (owner, repo, url, key)
    for issue in issues:
        repos = []
        for owner, repo in extract_repos(issue["body"]):
            key = f"{owner.lower()}/{repo.lower()}"
            repos.append((owner, repo, canonical_url(owner, repo), key))
        issue_repos[issue["number"]] = repos

    # Net-new = not in README and not already claimed earlier this run.
    net_new = []            # dict(url, name placeholder, owner, repo, key)
    for issue in issues:
        for owner, repo, url, key in issue_repos[issue["number"]]:
            if key in existing or key in batch_seen:
                continue
            batch_seen.add(key)
            net_new.append({"owner": owner, "repo": repo, "url": url, "key": key})

    # Quota guard: never call the model when there is nothing net-new.
    placements = {}         # url -> {"category": h} | {"new_category": ...} | {"gone": True}
    if net_new:
        tools = []
        for item in net_new:
            meta = fetch_metadata(item["owner"], item["repo"])
            if meta is None:
                placements[item["url"]] = {"gone": True}
                continue
            item["meta"] = meta
            tools.append({"url": item["url"], "name": meta["name"],
                          "description": meta["description"] or "No description"})
        if tools:
            placements.update(categorize(tools, categories))

    # Build insertions (only tools placed into an existing category).
    entries_by_category = {}
    added_names = []
    for item in net_new:
        place = placements.get(item["url"])
        if place and "category" in place:
            entry = format_entry(item["meta"], item["url"])
            entries_by_category.setdefault(place["category"], []).append(entry)
            added_names.append(item["meta"]["name"])

    if entries_by_category:
        readme = insert_entries(readme, entries_by_category)
        with open(README, "w", encoding="utf-8") as fh:
            fh.write(readme)
        git_commit(added_names)

    _finalize_issues(issues, issue_repos, existing, placements)
    print(f"Done. Added {len(added_names)} tool(s).")


def _finalize_issues(issues, issue_repos, existing, placements):
    for issue in issues:
        number = issue["number"]
        added, dupes, gone, pending = [], [], [], []
        for owner, repo, url, key in issue_repos[number]:
            place = placements.get(url)
            if key in existing:
                dupes.append(url)
            elif place and "category" in place:
                added.append(url)
            elif place and "new_category" in place:
                pending.append((url, place["new_category"]))
            elif place and place.get("gone"):
                gone.append(url)
            else:
                dupes.append(url)   # claimed earlier this run as a duplicate

        if not issue_repos[number]:
            comment(number, "No GitHub repo URLs found — please add the link(s) manually.")

        lines = []
        if added:
            lines.append("✅ Added:\n" + "\n".join(f"- {u}" for u in added))
        if dupes:
            lines.append("↩️ Already listed, skipped:\n" + "\n".join(f"- {u}" for u in dupes))
        if gone:
            lines.append("⚠️ Repo not found (404), skipped:\n" + "\n".join(f"- {u}" for u in gone))
        if pending:
            sugg = "\n".join(
                f"- {u} → suggested category **{nc['name']}** "
                f"(under {nc.get('macro_section', '?')})"
                for u, nc in pending
            )
            lines.append("🆕 No existing category fit — your call:\n" + sugg)

        if lines:
            comment(number, "\n\n".join(lines))

        if pending:
            relabel(number, INBOX_LABEL, NEEDS_LABEL)   # keep open for human decision
        else:
            relabel(number, INBOX_LABEL, DONE_LABEL)
            close_issue(number)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:                            # fail-closed: no partial state
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
