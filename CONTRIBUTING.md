# Contributing

Thanks for helping grow this AI-tools list! There are two ways to contribute a
resource. **The inbox flow is the easy one** — you don't need to edit any files.

---

## 1. The easy way — open an inbox Issue 📥

1. [**Open a new Issue**](../../issues/new).
2. Paste one or more **GitHub repository URLs** into the body (one per line). The
   title can be anything.
3. Add the **`inbox`** label.

That's it. A scheduled job (runs daily, and can be triggered manually) will:

- pull the repo's **description** and **primary language** from the GitHub API,
- pick the right category by where the tool fits in an **agent workflow**,
- append it to [`README.md`](README.md) in the matching section,
- comment a summary on your Issue and **close** it.

### Good to know

- **One Issue can list many URLs** — they're all processed together.
- **Duplicates are skipped** automatically (if the repo is already in the README,
  the Issue is closed with an "already listed" note).
- **Only GitHub repo URLs are auto-added.** Articles, blogs, and other links are
  flagged in a comment for a maintainer to add by hand.
- **No matching category?** If the bot thinks none of the existing categories fit,
  it does **not** guess. It relabels the Issue **`needs-category`**, keeps it open,
  and comments with a suggested category for a maintainer to decide. Adding a brand
  new section is always a human decision.

### Labels used by the flow

| Label | Meaning |
|-------|---------|
| `inbox` | Queued for the next run. **Add this to contribute.** |
| `done` | Processed and added to the README (Issue closed). |
| `needs-category` | The bot couldn't place it; awaiting a maintainer's decision. |

---

## 2. The direct way — edit `README.md` via Pull Request ✍️

`README.md` is the **single source of truth** — all tools, links, and notes live
there and nowhere else (see [`AGENTS.md`](AGENTS.md) for the full rule). If you'd
rather add the entry yourself, edit `README.md` directly and open a PR.

Match the existing entry format and drop it under the most fitting `##` section:

```markdown
- **ToolName** — One-line description of what it does. `PrimaryLanguage`
  <br/>https://github.com/owner/repo
```

- Categories are organized **by function in an agent workflow** (e.g. "where does
  this sit when an agent runs?"), not by form factor (skill / framework / CLI).
- Don't create new files or directories for content — everything goes in
  `README.md`. New top-level categories are welcome when something genuinely
  doesn't fit; add the `##` heading and a matching entry in the table of contents.

---

Both paths end in the same place: a tidy, categorized `README.md`. Pick whichever
is less friction for you. 🙌
