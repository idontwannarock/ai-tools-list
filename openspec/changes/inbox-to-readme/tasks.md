## 1. Processing script

- [ ] 1.1 Create `.github/scripts/inbox_to_readme.py` skeleton with config constants (label names, `BATCH_SIZE=20`, default model id) reading `GITHUB_TOKEN`/`GITHUB_REPOSITORY` from env
- [ ] 1.2 List open Issues labeled `inbox` via the GitHub API and extract `github.com/owner/repo` URLs from each body (record which Issue each URL came from)
- [ ] 1.3 Parse existing `##` category headings and all existing repo URLs from `README.md`
- [ ] 1.4 Dedup candidates against README and within the batch; compute the net-new list
- [ ] 1.5 Quota guard: if net-new is empty, skip the model call, comment "already listed"/close all-duplicate Issues, exit without committing
- [ ] 1.6 Fetch description + primary language per net-new repo via the GitHub API; format entries (omit language code when absent)
- [ ] 1.7 Chunk net-new tools into groups of `BATCH_SIZE` and call GitHub Models per chunk, requesting JSON: per tool → existing category heading OR new-category suggestion (name + macro-section)
- [ ] 1.8 Validate each returned category against the parsed heading set; unknown-and-not-flagged → fail the run (no commit)
- [ ] 1.9 Insert fitting entries at the end of the matching `##` section's bullet list
- [ ] 1.10 Collect new-category suggestions separately (do not insert)
- [ ] 1.11 Commit inserted entries to `main` in one commit whose message enumerates added tools; make no commit on failure
- [ ] 1.12 Issue lifecycle: close fully-processed Issues with a summary comment (relabel `inbox`→`done`); relabel Issues with pending suggestions `inbox`→`needs-category`, keep open, comment the suggestion

## 2. Workflow

- [ ] 2.1 Create `.github/workflows/inbox-to-readme.yml` with `on: schedule` (`0 18 * * *`) + `workflow_dispatch`
- [ ] 2.2 Set `permissions: contents: write, issues: write, models: read` and configure git author for the commit
- [ ] 2.3 Checkout, set up Python, run the script with `GITHUB_TOKEN` in env

## 3. Verification

- [ ] 3.1 Lint/parse-check the Python script and YAML workflow
- [ ] 3.2 Dry-run the dedup + formatting logic against the current `README.md` to confirm entry format matches existing bullets
- [ ] 3.3 Document one-time prerequisites (enable GitHub Models; create labels `inbox`, `done`, `needs-category`) — fold into the workflow file header comment, not a new content file
