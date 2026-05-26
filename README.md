# AI Tools List

個人 AI 工具收藏倉庫 — 用來治療 AI tool FOMO，集中記錄看到的工具、資源、文章。

> **整理規則**：本倉庫的**所有**資料、工具、連結、筆記都只寫在這份 `README.md`。
> 不要另外建立 `docs/`、`tools/`、其他 `.md` 檔或子目錄來放內容。
> 詳細的 AI agent 規範請見 [`AGENTS.md`](AGENTS.md)（Claude Code 透過 `.claude/CLAUDE.md` import 載入）。

分類原則：**按 agent workflow 中的功能位置**分，而非「skill / framework / cli」這類形式分類，方便「我需要 X 時找哪個」式查找。

---

## 目錄

- [Coding Agents / IDEs](#coding-agents--ides)
- [Agent Frameworks](#agent-frameworks)
- [Protocols & Specs](#protocols--specs)
- [Code Knowledge Graphs](#code-knowledge-graphs)
- [Agent Memory & Context Layers](#agent-memory--context-layers)
- [Web → Markdown for LLMs](#web--markdown-for-llms)
- [Prompting Tricks & Token Hacks](#prompting-tricks--token-hacks)
- [Diff & Review Viewers](#diff--review-viewers)
- [Agent DevTools / Inspection](#agent-devtools--inspection)
- [Skill Authoring & Validation](#skill-authoring--validation)
- [Skill Collections & Reference Configs](#skill-collections--reference-configs)
- [Curated Lists / Awesome](#curated-lists--awesome)
- [NotebookLM Bridges](#notebooklm-bridges)
- [Workflow & SDLC for AI Coding](#workflow--sdlc-for-ai-coding)
- [Specialized Skills](#specialized-skills)
- [Learning Resources](#learning-resources)
- [Others](#others)

---

## Coding Agents / IDEs

- **OpenClaw** — Cross-platform personal AI assistant (any OS / any platform). `TypeScript`
  <br/>https://github.com/openclaw/openclaw

## Agent Frameworks

- **Mastra** — TypeScript framework for building AI agents; tool use, workflows, RAG, evals.
  <br/>https://mastra.ai/docs
- **WFGY (Polaris Protocol)** — Open-source toolkit for AI reasoning, RAG, agents and real-world workflows; includes Problem Map and Global Debug Card. `Jupyter Notebook`
  <br/>https://github.com/onestardao/WFGY

## Protocols & Specs

- **Agent Client Protocol (ACP)** — Open protocol standardizing communication between editors/IDEs and coding agents so any editor can talk to any agent. `Rust`
  <br/>Repo: https://github.com/agentclientprotocol/agent-client-protocol
  <br/>Docs: https://agentclientprotocol.com/get-started/introduction
- **OpenAB** — Lightweight, secure, cloud-native ACP harness that bridges Discord with any ACP-compatible coding CLI. `Rust`
  <br/>https://github.com/openabdev/openab
- **OpenCLI** — The OpenCLI Specification and tooling repository (standard way to describe CLI surfaces). `Go`
  <br/>https://github.com/bcdxn/opencli

## Code Knowledge Graphs

Pre-index a repo into a graph so the agent reads only what matters — fewer tokens, fewer tool calls.

- **codegraph (colbymchenry)** — Pre-indexed code knowledge graph for Claude Code, Codex, Cursor, OpenCode, Hermes; 100% local. `TypeScript`
  <br/>https://github.com/colbymchenry/codegraph
- **code-review-graph (tirth8205)** — Local-first code intelligence graph for MCP and CLI; persistent map with benchmarked context reductions on reviews and large repos. `Python`
  <br/>https://github.com/tirth8205/code-review-graph
- **graphify (safishamsi)** — Agent skill that turns any folder (code, SQL schemas, R scripts, docs, papers, images, video) into a queryable knowledge graph. `Python`
  <br/>https://github.com/safishamsi/graphify
- **GitNexus** — Zero-server, browser-based code knowledge graph + built-in Graph RAG agent; drop a GitHub repo or ZIP. `TypeScript`
  <br/>https://github.com/abhigyanpatwari/GitNexus

## Agent Memory & Context Layers

- **mnemon** — LLM-supervised persistent memory for AI agents; graph-based recall, cross-session knowledge, single binary. `Go`
  <br/>https://github.com/mnemon-dev/mnemon
- **lean-ctx (Lean Cortex)** — Cognitive context layer for agentic systems: 51+ MCP tools, 10 read modes, 95+ shell patterns, up to 99% token savings. `Rust`
  <br/>https://github.com/yvgude/lean-ctx

## Web → Markdown for LLMs

- **markdown.new** — Free tool that converts any URL into clean, AI-ready Markdown with much smaller token footprint than raw HTML.
  <br/>https://markdown.new/
- **Cloudflare — Markdown for Agents** — Cloudflare feature that auto-converts HTML to Markdown in real time when agents request it with the right headers; up to ~80% token reduction.
  <br/>https://blog.cloudflare.com/markdown-for-agents/

## Prompting Tricks & Token Hacks

- **caveman** — 🪨 Claude Code skill that cuts ~65% of tokens by making the agent talk like a caveman. `JavaScript`
  <br/>https://github.com/juliusbrussee/caveman
- **pua** — 高能動性 skill：把 agent 當成被定 P8 然後丟進 PIP 的工程師來激勵；30 天提升表現 (中文)。 `TypeScript`
  <br/>https://github.com/tanweai/pua

## Diff & Review Viewers

- **difftastic** — Syntax-aware structural diff written in Rust 🟥🟩. `Rust`
  <br/>https://github.com/Wilfred/difftastic
- **diffity** — GitHub-style diff viewer for reviewing code changes from Claude Code, Cursor and other AI tools. `TypeScript`
  <br/>https://github.com/nilbuild/diffity

## Agent DevTools / Inspection

- **claude-devtools** — The missing DevTools for Claude Code: inspect session logs, tool calls, token usage, subagents and context window in a visual UI. `TypeScript`
  <br/>https://github.com/matt1398/claude-devtools

## Skill Authoring & Validation

- **skills-best-practices (mgechev)** — Write professional-grade skills for agents, validate them using LLMs, maintain a lean context window. `Python`
  <br/>https://github.com/mgechev/skills-best-practices
- **skill-scanner (cisco-ai-defense)** — Security scanner for agent skills. `Python`
  <br/>https://github.com/cisco-ai-defense/skill-scanner

## Skill Collections & Reference Configs

- **mattpocock/skills** — Matt Pocock's personal `.claude/` skills directory ("Skills for Real Engineers"). `Shell`
  <br/>https://github.com/mattpocock/skills
- **claude-code-showcase (ChrisWiles)** — Comprehensive Claude Code project configuration example covering hooks, skills, agents, commands, and GitHub Actions. `JavaScript`
  <br/>https://github.com/ChrisWiles/claude-code-showcase

## Curated Lists / Awesome

- **awesome-claude-skills (ComposioHQ)** — Curated list of awesome Claude Skills, resources, and tools for customizing Claude AI workflows. `Python`
  <br/>https://github.com/ComposioHQ/awesome-claude-skills
- **awesome-agent-skills (heilcheng)** — Tutorials, guides, and a curated directory of agent skills. `TypeScript`
  <br/>https://github.com/heilcheng/awesome-agent-skills

## NotebookLM Bridges

- **notebooklm-skill (PleasePrompto)** — Claude Code skill that drives Google NotebookLM via browser automation; source-grounded, citation-backed answers from Gemini. `Python`
  <br/>https://github.com/PleasePrompto/notebooklm-skill
- **notebooklm-py (teng-lin)** — Unofficial Python API + agentic skill for NotebookLM (incl. features the web UI doesn't expose); usable from Python, CLI, Claude Code, Codex, OpenClaw. `Python`
  <br/>https://github.com/teng-lin/notebooklm-py

## Workflow & SDLC for AI Coding

- **aidlc-workflows (awslabs)** — AI-Driven Life Cycle (AI-DLC) adaptive workflow steering rules for AI coding agents. `Python`
  <br/>https://github.com/awslabs/aidlc-workflows

## Specialized Skills

Single-purpose Claude Code skills with a clear functional niche.

- **codebase-to-course** — Skill that turns any codebase into a beautiful, interactive single-page HTML course for non-technical readers. `CSS`
  <br/>https://github.com/zarazhangrui/codebase-to-course
- **sera-cli (allenai)** — Use the Ai2 Open Coding Agents SERA (Soft-Verified Efficient Repository Agents) model from inside Claude Code. `Python`
  <br/>https://github.com/allenai/sera-cli

## Learning Resources

- **vibe-coding-cn** — 中文 vibe coding 資源 / 教學集。 `Python`
  <br/>https://github.com/2025Emma/vibe-coding-cn

## Others

_(尚未新增)_
