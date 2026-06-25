# AI Tools List

個人 AI 工具收藏倉庫 — 用來治療 AI tool FOMO，集中記錄看到的工具、資源、文章。

> **整理規則**：本倉庫的**所有**資料、工具、連結、筆記都只寫在這份 `README.md`。
> 不要另外建立 `docs/`、`tools/`、其他 `.md` 檔或子目錄來放內容。
> 詳細的 AI agent 規範請見 [`AGENTS.md`](AGENTS.md)（Claude Code 透過 `.claude/CLAUDE.md` import 載入）。

分類原則：**按 agent workflow 中的功能位置**分，而非「skill / framework / cli」這類形式分類，方便「我需要 X 時找哪個」式查找。

---

## 目錄

**Runtime / 基礎建設**
- [Coding Agents / IDEs](#coding-agents--ides)
- [Agent Frameworks](#agent-frameworks)
- [LLM Inference Engines](#llm-inference-engines)
- [Protocols & Specs](#protocols--specs)
- [MCP Servers / Tools](#mcp-servers--tools)

**給 agent 看的 context**
- [Code Knowledge Graphs](#code-knowledge-graphs)
- [Agent Memory & Context Layers](#agent-memory--context-layers)
- [Vector Search / RAG Infrastructure](#vector-search--rag-infrastructure)
- [Web → Markdown for LLMs](#web--markdown-for-llms)
- [Web Crawling & External Data for Agents](#web-crawling--external-data-for-agents)
- [OCR / Document Extraction](#ocr--document-extraction)

**省 token / 控制成本**
- [Token-Saving Proxies](#token-saving-proxies)
- [Prompting Tricks & Fun Skills](#prompting-tricks--fun-skills)

**觀察 / Debug / Review**
- [Diff & Review Viewers](#diff--review-viewers)
- [Agent DevTools / Inspection](#agent-devtools--inspection)

**Agent patterns / safety**
- [Autonomous Loops / Research Agents](#autonomous-loops--research-agents)
- [Sandboxing / Secure Execution](#sandboxing--secure-execution)

**Skill 生態**
- [Skill Authoring & Validation](#skill-authoring--validation)
- [Skill Collections & Reference Configs](#skill-collections--reference-configs)
- [Curated Lists / Awesome](#curated-lists--awesome)

**整合 / 應用**
- [NotebookLM Bridges](#notebooklm-bridges)
- [OpenClaw Integrations](#openclaw-integrations)
- [Workflow & SDLC for AI Coding](#workflow--sdlc-for-ai-coding)
- [Specialized Skills](#specialized-skills)

**評估 / 學習**
- [Evaluation Frameworks](#evaluation-frameworks)
- [Learning Resources](#learning-resources)
- [Others](#others)

---

## Coding Agents / IDEs

- **OpenClaw** — Cross-platform personal AI assistant (any OS / any platform). `TypeScript`
  <br/>https://github.com/openclaw/openclaw
- **Pane** — Terminal-first AI agent **manager** ("Superhuman for agents"); you bring agents, Pane makes them fly. `TypeScript`
  <br/>https://github.com/dcouple/Pane
- **paseo** — Coding agents from your phone, desktop and CLI. `TypeScript`
  <br/>https://github.com/getpaseo/paseo

## Agent Frameworks

- **Mastra** — TypeScript framework for building AI agents; tool use, workflows, RAG, evals.
  <br/>https://mastra.ai/docs
- **WFGY (Polaris Protocol)** — Open-source toolkit for AI reasoning, RAG, agents and real-world workflows; includes Problem Map and Global Debug Card. `Jupyter Notebook`
  <br/>https://github.com/onestardao/WFGY

## LLM Inference Engines

- **JittorLLMs** — 計圖大模型推理庫，高效能、低硬體需求、中文支援良好、可移植。 `Python`
  <br/>https://github.com/Jittor/JittorLLMs

## Protocols & Specs

- **Agent Client Protocol (ACP)** — Open protocol standardizing communication between editors/IDEs and coding agents so any editor can talk to any agent. `Rust`
  <br/>Repo: https://github.com/agentclientprotocol/agent-client-protocol
  <br/>Docs: https://agentclientprotocol.com/get-started/introduction
- **OpenAB** — Lightweight, secure, cloud-native ACP harness that bridges Discord with any ACP-compatible coding CLI. `Rust`
  <br/>https://github.com/openabdev/openab
- **OpenCLI** — The OpenCLI Specification and tooling repository (standard way to describe CLI surfaces). `Go`
  <br/>https://github.com/bcdxn/opencli

## MCP Servers / Tools

- **mercury-mcp** — Cross-architecture LLM internal observation database (23 models, 13 architecture families) exposed as MCP tools for any AI coding agent. `Python`
  <br/>https://github.com/norika1207-lab/mercury-mcp

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
- **cx (ind-igo)** — Semantic code navigation for AI agents. `Rust`
  <br/>https://github.com/ind-igo/cx

## Agent Memory & Context Layers

Persistent memory across sessions + active session context optimization.

- **mnemon** — LLM-supervised persistent memory; graph-based recall, cross-session knowledge, single binary. `Go`
  <br/>https://github.com/mnemon-dev/mnemon
- **mempalace** — Best-benchmarked open-source AI memory system. `Python`
  <br/>https://github.com/MemPalace/mempalace
- **episodic-memory (obra)** — Episodic memory implementation. `TypeScript`
  <br/>https://github.com/obra/episodic-memory
- **claude-memory-engine** — Claude Code 的記憶系統，hooks + markdown 實作，零依賴。 `JavaScript`
  <br/>https://github.com/HelloRuru/claude-memory-engine
- **kernel-memory (Microsoft)** — Memory solution for users, teams, and applications. `C#`
  <br/>https://github.com/microsoft/kernel-memory
- **lean-ctx (Lean Cortex)** — Cognitive context layer: 51+ MCP tools, 10 read modes, 95+ shell patterns, up to 99% token savings. `Rust`
  <br/>https://github.com/yvgude/lean-ctx
- **cozempic** — Context cleaning for Claude Code; prune bloated sessions, protect Agent Teams from context loss, tiered auto-guard. `Python`
  <br/>https://github.com/Ruya-AI/cozempic
- **Remio** — Local-first AI memory and personal knowledge-base client; its CLI and agent skill let agents query indexed files, webpages, recordings, emails, messages, images, and notes instead of repeatedly scanning folders or loading whole documents into prompts. Requires the Remio desktop app/client.
  <br/>https://remio.ai/

## Vector Search / RAG Infrastructure

- **faiss (Meta)** — Library for efficient similarity search and clustering of dense vectors. `C++`
  <br/>https://github.com/facebookresearch/faiss

## Web → Markdown for LLMs

- **markdown.new** — Free tool that converts any URL into clean, AI-ready Markdown with much smaller token footprint than raw HTML.
  <br/>https://markdown.new/
- **Cloudflare — Markdown for Agents** — Auto-converts HTML to Markdown in real time when agents request it with the right headers; up to ~80% token reduction.
  <br/>https://blog.cloudflare.com/markdown-for-agents/
- **markitdown (Microsoft)** — Python tool for converting files and office documents (Word/PPT/PDF/…) to Markdown. `Python`
  <br/>https://github.com/microsoft/markitdown

## Web Crawling & External Data for Agents

- **crawl4ai** — 🚀🤖 Open-source LLM-friendly web crawler & scraper. `Python`
  <br/>https://github.com/unclecode/crawl4ai
- **Agent-Reach** — Give your agent eyes to see the entire internet: Twitter, Reddit, YouTube, GitHub, Bilibili, 小紅書 — one CLI, zero API fees. `Python`
  <br/>https://github.com/Panniantong/Agent-Reach

## OCR / Document Extraction

- **PaddleOCR** — Turn any PDF/image into structured data for AI; 100+ languages. `Python`
  <br/>https://github.com/PaddlePaddle/PaddleOCR
- **PPOCRLabel** — Semi-automatic graphic annotation tool for OCR, built-in PP-OCR model. `Python`
  <br/>https://github.com/PFCCLab/PPOCRLabel
- **imagepdf2txt (joshhu)** — 用 PaddleOCR 將圖片型 PDF 檔案轉換成純文字。 `Python`
  <br/>https://github.com/joshhu/imagepdf2txt

## Token-Saving Proxies

- **rtk (rtk-ai)** — CLI proxy that reduces LLM token consumption by 60-90% on common dev commands; single Rust binary, zero deps. `Rust`
  <br/>https://github.com/rtk-ai/rtk

## Prompting Tricks & Fun Skills

- **caveman** — 🪨 Claude Code skill that cuts ~65% of tokens by making the agent talk like a caveman. `JavaScript`
  <br/>https://github.com/juliusbrussee/caveman
- **pua** — 高能動性 skill：把 agent 當成被定 P8 然後丟進 PIP 的工程師激勵；30 天提升表現 (中文)。 `TypeScript`
  <br/>https://github.com/tanweai/pua

## Diff & Review Viewers

- **difftastic** — Syntax-aware structural diff written in Rust 🟥🟩. `Rust`
  <br/>https://github.com/Wilfred/difftastic
- **diffity** — GitHub-style diff viewer for reviewing code changes from Claude Code, Cursor and other AI tools. `TypeScript`
  <br/>https://github.com/nilbuild/diffity

## Agent DevTools / Inspection

- **claude-devtools** — The missing DevTools for Claude Code: inspect session logs, tool calls, token usage, subagents and context window in a visual UI. `TypeScript`
  <br/>https://github.com/matt1398/claude-devtools
- **ccstory** — Claude Code usage recap with narrative — "ccusage tells you the bill, ccstory tells the story." `Python`
  <br/>https://github.com/atomchung/ccstory
- **cc-mirror** — Create multiple isolated Claude Code variants with custom providers (Z.ai, MiniMax, OpenRouter, LiteLLM). `TypeScript`
  <br/>https://github.com/numman-ali/cc-mirror

## Autonomous Loops / Research Agents

- **ralph** — Autonomous AI agent loop that runs repeatedly until all PRD items are complete. `TypeScript`
  <br/>https://github.com/snarktank/ralph
- **karpathy/autoresearch** — AI agents running research on single-GPU nanochat training automatically. `Python`
  <br/>https://github.com/karpathy/autoresearch
- **pi-autoresearch (davebcn87)** — Autonomous experiment loop extension for `pi`. `TypeScript`
  <br/>https://github.com/davebcn87/pi-autoresearch

## Sandboxing / Secure Execution

- **secure-exec (rivet)** — Secure Node.js execution without a sandbox; lightweight, npm-compatible, no containers/VMs. `JavaScript`
  <br/>https://github.com/rivet-dev/secure-exec

## Skill Authoring & Validation

- **skills-best-practices (mgechev)** — Write professional-grade skills for agents, validate them using LLMs, maintain a lean context window. `Python`
  <br/>https://github.com/mgechev/skills-best-practices
- **skill-scanner (cisco-ai-defense)** — Security scanner for agent skills. `Python`
  <br/>https://github.com/cisco-ai-defense/skill-scanner

## Skill Collections & Reference Configs

Personal / branded `.claude/` directories and `CLAUDE.md` references worth borrowing from.

- **mattpocock/skills** — Matt Pocock's personal `.claude/` skills directory ("Skills for Real Engineers"). `Shell`
  <br/>https://github.com/mattpocock/skills
- **claude-code-showcase (ChrisWiles)** — Comprehensive Claude Code project configuration example covering hooks, skills, agents, commands, and GitHub Actions. `JavaScript`
  <br/>https://github.com/ChrisWiles/claude-code-showcase
- **gstack (Garry Tan)** — Garry Tan's exact Claude Code setup: 23 opinionated tools playing CEO / Designer / Eng Manager / Release Manager / Doc Engineer / QA. `TypeScript`
  <br/>https://github.com/garrytan/gstack
- **andrej-karpathy-skills (multica-ai)** — A single `CLAUDE.md` derived from Andrej Karpathy's observations on LLM coding pitfalls.
  <br/>https://github.com/multica-ai/andrej-karpathy-skills
- **contains-studio/agents** — Sharing current agents in use (community-shared agent set).
  <br/>https://github.com/contains-studio/agents

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

## OpenClaw Integrations

- **Line-for-openclaw (enzotseng-ops)** — Line integration for OpenClaw. `JavaScript`
  <br/>https://github.com/enzotseng-ops/Line-for-openclaw

## Workflow & SDLC for AI Coding

- **aidlc-workflows (awslabs)** — AI-Driven Life Cycle (AI-DLC) adaptive workflow steering rules for AI coding agents. `Python`
  <br/>https://github.com/awslabs/aidlc-workflows

## Specialized Skills

Single-purpose skills with a clear functional niche.

- **codebase-to-course** — Skill that turns any codebase into a beautiful, interactive single-page HTML course for non-technical readers. `CSS`
  <br/>https://github.com/zarazhangrui/codebase-to-course
- **sera-cli (allenai)** — Use the Ai2 Open Coding Agents SERA (Soft-Verified Efficient Repository Agents) model from inside Claude Code. `Python`
  <br/>https://github.com/allenai/sera-cli
- **colleague-skill (titanwings)** — 「数字生命 1.0」— 把冰冷的離別轉化成溫暖的 skill。 `Python`
  <br/>https://github.com/titanwings/colleague-skill

## Evaluation Frameworks

- **oss-investment-scorecard (lucy-cxy)** — 5-dimension scoring framework for evaluating OSS AI projects from a VC investment perspective; maintained by Lucy Chen (EIR @ Zoo Capital).
  <br/>https://github.com/lucy-cxy/oss-investment-scorecard

## Learning Resources

- **vibe-coding-cn** — 中文 vibe coding 資源 / 教學集。 `Python`
  <br/>https://github.com/2025Emma/vibe-coding-cn
- **learn-claude-code (shareAI-lab)** — "Bash is all you need" — a nano Claude Code–like agent harness, built from 0 to 1. `Python`
  <br/>https://github.com/shareAI-lab/learn-claude-code

## Others

- **DeepSRT/roadmap** — DeepSRT public roadmap.
  <br/>https://github.com/DeepSRT/roadmap
