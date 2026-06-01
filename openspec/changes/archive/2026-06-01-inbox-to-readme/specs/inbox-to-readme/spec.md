## ADDED Requirements

### Requirement: Issue-based inbox collection
The system SHALL treat any open GitHub Issue labeled `inbox` as a capture point, extracting GitHub repository URLs from the Issue body. A single Issue MAY contain multiple URLs.

#### Scenario: Issue with one repo URL
- **WHEN** an open Issue labeled `inbox` has a body containing `https://github.com/owner/repo`
- **THEN** the system extracts that URL as a candidate tool

#### Scenario: Issue with multiple repo URLs
- **WHEN** an open Issue labeled `inbox` body contains several GitHub repo URLs
- **THEN** the system extracts every distinct repo URL as a separate candidate

#### Scenario: Non-GitHub URL in body
- **WHEN** an Issue body contains a non-GitHub URL (e.g. a blog or docs link)
- **THEN** the system does not treat it as a tool and the closing comment notes it must be added manually

### Requirement: Scheduled batch processing
The system SHALL run on a daily cron schedule and SHALL also be triggerable manually via `workflow_dispatch`. Each run processes all open `inbox` Issues in one batch.

#### Scenario: Daily scheduled run
- **WHEN** the cron schedule fires
- **THEN** the workflow collects all open `inbox` Issues and processes them in a single batch run

#### Scenario: Manual trigger
- **WHEN** a maintainer triggers the workflow via `workflow_dispatch`
- **THEN** the workflow runs immediately with the same behavior as the scheduled run

### Requirement: Dedup before model call (quota guard)
The system SHALL deduplicate candidate URLs against the current `README.md` and within the batch BEFORE invoking GitHub Models, and SHALL skip the model call entirely when no net-new tools remain.

#### Scenario: All candidates already listed
- **WHEN** every extracted URL already appears in `README.md`
- **THEN** the system does not call GitHub Models, makes no commit, and comments on each affected Issue that its links already exist before closing it

#### Scenario: Duplicate URLs within one batch
- **WHEN** the same repo URL appears in two different `inbox` Issues in the same run
- **THEN** the system keeps a single net-new entry and does not insert the tool twice

#### Scenario: At least one net-new tool
- **WHEN** one or more extracted URLs are absent from `README.md` after dedup
- **THEN** the system proceeds to fetch metadata and call GitHub Models for the net-new tools only

### Requirement: Metadata fetch and entry format
For each net-new repo the system SHALL fetch the description and primary language via the GitHub API using the built-in token, and SHALL format the README entry as a bullet matching the existing convention.

#### Scenario: Entry formatting
- **WHEN** a net-new repo has description "D" and primary language "L" at `https://github.com/owner/repo`
- **THEN** the inserted entry is `- **repo** — D. \`L\`` followed by `  <br/>https://github.com/owner/repo`

#### Scenario: Repo without a detected language
- **WHEN** the GitHub API returns no primary language for a repo
- **THEN** the system omits the trailing language code rather than emitting an empty backtick pair

### Requirement: Category assignment via GitHub Models
The system SHALL use GitHub Models (authenticated by the built-in `GITHUB_TOKEN` with `models: read`) to assign each net-new tool to one of the existing `##` category headings in `README.md`, with no external API key.

#### Scenario: Tool matches an existing category
- **WHEN** the model assigns a net-new tool to an existing `##` heading
- **THEN** the system inserts the formatted entry at the end of that section's bullet list

#### Scenario: Model returns an unknown category
- **WHEN** the model returns a category name that does not match any existing `##` heading and does not flag it as a new-category suggestion
- **THEN** the system treats the run as failed for safety (no partial commit) so the batch can be retried

### Requirement: Batching for large inboxes
The system SHALL chunk net-new tools into groups of at most a configured batch size (default 20) per GitHub Models request so that a large inbox never overflows the model context window.

#### Scenario: Inbox larger than batch size
- **WHEN** there are more net-new tools than the batch size
- **THEN** the system issues multiple model requests, one per chunk, and accumulates the results

### Requirement: Human-gated new-category suggestions
When the model judges that no existing category fits a tool, the system SHALL NOT auto-insert the tool or auto-create a category. Instead it SHALL record the suggestion for human decision.

#### Scenario: Model suggests a new category
- **WHEN** the model marks a net-new tool as needing a new category
- **THEN** the system does not insert that tool into `README.md`, relabels the Issue from `inbox` to `needs-category`, keeps it open, and comments with the suggested category name, target macro-section, and formatted entry

#### Scenario: Issue mixing fitting and non-fitting tools
- **WHEN** one Issue contains some tools that fit existing categories and some that need a new category
- **THEN** the system inserts the fitting tools, keeps the Issue open under `needs-category`, and comments listing both what was added and the pending new-category suggestions

### Requirement: Issue lifecycle
The system SHALL close Issues that were fully processed and SHALL leave Issues with pending new-category decisions open.

#### Scenario: Fully processed Issue
- **WHEN** every tool in an Issue was either inserted or skipped as a duplicate
- **THEN** the system comments a summary and closes the Issue (relabeled `inbox` → `done`)

#### Scenario: Issue awaiting a category decision
- **WHEN** an Issue still has at least one tool needing a new category
- **THEN** the system leaves the Issue open under the `needs-category` label and does not relabel it `done`

### Requirement: Atomic commit with auditable history
The system SHALL commit inserted entries directly to `main` in a single commit whose message lists the added tools, and SHALL make no commit when a run fails partway.

#### Scenario: Successful batch
- **WHEN** one or more tools are inserted in a run
- **THEN** the system creates exactly one commit to `main` whose message enumerates the added tools

#### Scenario: Failure during a run
- **WHEN** metadata fetch or a model request fails for a chunk
- **THEN** the system aborts without committing and leaves the affected Issues labeled `inbox` so the next run retries them
