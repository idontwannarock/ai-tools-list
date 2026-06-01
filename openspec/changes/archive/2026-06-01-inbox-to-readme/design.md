## Context

`README.md` is the single source of truth for this repo (enforced by `AGENTS.md` README-only rule). Tools are grouped by their position in an agent workflow, not by form factor, so choosing a category requires reading the semantics of the existing headings — a judgment task. Adding a tool today is a manual README edit. We want a near-zero-effort capture point usable from a phone, with the organizing work done on a schedule in the cloud.

Constraints:
- README-only rule allows new `.github/` infrastructure files but forbids new content files/dirs.
- Maintainer prefers pure-cloud execution, a daily batch (not per-event), direct commit to `main`, and no external API key.
- Categorization must not silently mangle the README's category structure.

## Goals / Non-Goals

**Goals:**
- Capture repo URLs by pasting them into a GitHub Issue labeled `inbox`.
- A daily scheduled GitHub Action that batch-processes the inbox: dedup → metadata → categorize → insert → commit.
- Zero external secrets — use GitHub Models via the built-in `GITHUB_TOKEN`.
- Never spend model quota when there is nothing net-new.
- Never overflow model context regardless of inbox size.
- Preserve, rather than discard or force, the model's suggestion when no category fits.

**Non-Goals:**
- Handling non-GitHub URLs (articles, blogs) — flagged for manual add only.
- Auto-creating new `##` categories (structural change stays human-gated).
- A web form / bot / per-issue real-time trigger.
- Editing existing entries or re-categorizing the existing list.

## Decisions

**D1. GitHub Models over Claude API or Copilot coding agent.**
GitHub Models runs inside a normal Action authenticated by `GITHUB_TOKEN` (`models: read`), so no external secret and it fits a cron batch. Claude API would need `ANTHROPIC_API_KEY`. Copilot coding agent is assignment-triggered ("one issue → one PR"), which does not match the daily-batch model and requires a Copilot subscription.

**D2. Dedup strictly before the model call.**
Making "don't waste quota" a structural property of the data flow (filter net-new first, then branch) rather than a post-hoc check guarantees the model is never called for an all-duplicate run.

**D3. Split deterministic vs. judgment work.**
The script does everything deterministic — extract URLs, dedup, fetch metadata, format entries, insert, commit. The model does exactly one thing: pick a category (or flag "none fits"). This minimizes the model's blast radius and makes its output trivially validatable against the known set of `##` headings.

**D4. New-category suggestions are human-gated via a label.**
On direct-commit-to-`main`, changing the README's skeleton unreviewed is too risky. When the model flags "no category fits", the tool is not inserted; the Issue is relabeled `inbox` → `needs-category`, kept open, and annotated with the suggestion. `needs-category` is excluded from the daily query, so it is neither reprocessed nor spammed.

**D5. Chunked model requests (default 20).**
Per-request context ≈ fixed heading list + N short tool descriptions. Chunking bounds context and localizes a failure to one chunk. Batch size is a script constant, easily tuned.

**D6. Atomic commit, fail-closed.**
A run either commits all its insertions in one commit (message enumerates added tools, enabling one-shot `git revert`) or, on any metadata/model failure, commits nothing and leaves Issues as `inbox` for the next run. No partial writes.

**D7. Idempotency via label transition.**
Processed Issues move `inbox` → `done` (and close) or `inbox` → `needs-category`. The daily query selects only open `inbox` Issues, so nothing is processed twice. README grep dedup is the second guard.

## Risks / Trade-offs

- **Model picks a wrong-but-valid category** → Direct-to-main means it lands unreviewed. Mitigation: commit message enumerates additions so a bad categorization is a one-commit `git revert`; entries are appended (never overwrite), so blast radius is additive only.
- **GitHub Models rate limits / outage** → Mitigation: fail-closed (D6); Issues stay `inbox` and retry next day.
- **Model hallucinates a non-existent heading without the new-category flag** → Mitigation: validate returned category against the parsed `##` set; unknown → treat run as failed rather than insert into a guessed section.
- **README heading parsing drift** (e.g. a heading renamed) → Mitigation: headings are parsed live from `README.md` each run, so the model always sees the current set.
- **GitHub Models availability for the account/repo** → One-time prerequisite: enable GitHub Models; documented in proposal Impact.

## Migration Plan

1. Merge `.github/workflows/inbox-to-readme.yml` and `.github/scripts/inbox_to_readme.py`.
2. One-time repo setup: enable GitHub Models; create labels `inbox`, `done`, `needs-category`.
3. Validate via `workflow_dispatch` against a test Issue before relying on the cron.
4. Rollback: delete/disable the workflow file; no data migration needed. README changes are normal commits, revertible individually.

## Open Questions

- Which specific GitHub Models model id to default to (a capable general model); set as a script constant and tunable without spec change.
