## Why

Collecting AI tools into this repo currently means hand-editing `README.md`: opening the file, picking the right workflow-function category, and matching the entry format. That friction means links seen on mobile or in passing get lost. We want a low-effort capture point (paste a repo URL into a GitHub Issue, even from a phone) and have the repo organize itself on a schedule.

## What Changes

- Add a **GitHub Issue–based inbox**: an Issue labeled `inbox` whose body contains one or more GitHub repo URLs is a capture point.
- Add a **scheduled GitHub Actions workflow** (daily cron + manual `workflow_dispatch`) that processes the inbox in batch.
- Add a **processing script** that: dedupes against the current README, fetches repo metadata (description, primary language) via the GitHub API, asks GitHub Models to assign each tool to an existing category, inserts formatted entries into the correct `##` section, and commits directly to `main`.
- Use **GitHub Models** (`models: read` + built-in `GITHUB_TOKEN`) for categorization — **no external API key**.
- **Quota guard**: the model is only called when there is at least one net-new tool after dedup.
- **Batching**: net-new tools are chunked (default 20/request) so large inboxes never overflow model context.
- **New-category suggestions are preserved**: when the model judges that no existing category fits, the tool is NOT auto-inserted; the Issue is relabeled `needs-category` and a comment records the model's suggested category + formatted entry for human decision.
- Processed Issues are commented on and **closed**; Issues needing a category decision stay open under `needs-category`.

## Capabilities

### New Capabilities
- `inbox-to-readme`: Issue-based collection of repo URLs that a scheduled job categorizes and writes into `README.md`, with dedup, quota-guarding, batching, and human-gated new-category suggestions.

### Modified Capabilities
<!-- None. No existing OpenSpec specs; README content rules in AGENTS.md are unchanged (this change only adds .github/ infrastructure). -->

## Impact

- **New files** (infrastructure, allowed by `AGENTS.md` README-only rule):
  - `.github/workflows/inbox-to-readme.yml`
  - `.github/scripts/inbox_to_readme.py`
- **Repo settings** (one-time, manual): enable GitHub Models for the repo; create labels `inbox`, `done`, `needs-category`.
- **Permissions**: workflow needs `contents: write`, `issues: write`, `models: read`. No external secrets.
- **`README.md`**: mutated automatically by the job (entries appended under existing `##` sections). Category structure is never auto-changed.
