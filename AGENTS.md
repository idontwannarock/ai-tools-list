# Agent Rules — ai-tools-list

This file follows the open `AGENTS.md` convention (Codex, Cursor, Aider, Continue, etc.).
Claude Code loads it via `@../AGENTS.md` import inside [`.claude/CLAUDE.md`](.claude/CLAUDE.md).

## Repository purpose

Personal collection of AI tools / resources to manage AI tool FOMO.

## 🚨 ABSOLUTE RULE — README-only

**All content (tools, links, notes, categories, descriptions) MUST be written into `README.md` at the repo root, and ONLY there.**

This rule applies to every AI agent and every human contributor. It is non-negotiable.

### Forbidden

- ❌ Creating new `*.md` files for content (no `tools.md`, `notes.md`, `awesome-*.md`, …)
- ❌ Creating content directories (`docs/`, `tools/`, `categories/`, `notes/`, …)
- ❌ Splitting categories into separate files
- ❌ Generating auxiliary indexes, sidebars, or JSON/YAML data files for content
- ❌ Creating per-tool README files

### Allowed

- ✅ Editing `README.md` (add / remove / re-categorize tools, restructure sections)
- ✅ Creating non-content infrastructure files when explicitly requested (`.gitignore`, CI configs, etc.)
- ✅ Updating this `AGENTS.md` itself when rules evolve

### When in doubt

If a request would require creating a new content file, **stop and ask the user first**. Default to folding it into a new section inside `README.md`.
