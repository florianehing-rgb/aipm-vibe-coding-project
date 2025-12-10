# Group Vibe-Coding Project Brief

Build and present a small, end-to-end application in groups of 2–3 using the [vibe-coding tools](#popular-vibe-coding-tools). The goal is rapid, AI-assisted delivery with clear prompts, minimal hand-coding, and a tight presentation.

### What to build
- Pick a simple but end-to-end app (e.g., habit tracker, mini ticket board, event RSVP, micro SaaS landing with signup). This can be a chance to prototype your capstone idea—don’t over-hunt for data. 
- Scope for 1–2 core user journeys; keep the rest as stretch goals.
- Favor AI IDE/CLI agents for glue code (VSCode Copilot, Cursor, OpenAI Codex CLI, Antigravity, Windsurf, Claude Code, Cline, OpenCode) and hosted AI builders for UI (v0, Lovable, Bolt.new, Emergent).
- Most tools have free tiers; you can try multiple without paying.

### Process
1) Formation & setup: Create a repo, assign roles (Driver, Prompt Engineer, QA/Tester, Presenter). Rotate Driver/Prompt Engineer mid-way.  
2) Tooling: Choose at least two tools from the table. Note why you picked them.
3) Prompting: Ask chatbots to draft strong prompts for what you want to do. Use [`AGENTS.md`](AGENTS.md) to store and update project instructions (see https://agents.md).
4) Build loops: Ship in short cycles (plan → prompt → review → adjust). Keep manual edits minimal; prefer refining prompts.  
5) Testing: Add quick checks (e.g., smoke test script, manual checklist).  
6) Polish: Add basic styling or data fixtures so the demo feels real.  
7) Presentation prep: Dry-run the demo; ensure repo instructions work on a clean machine.

### Deliverables (due at presentation)
- Running app with clear start instructions in `README.md` (or link to hosted preview).  
- `AGENTS.md` with instructions for the AI tools.
- A 5-minute live demo covering: problem, user journey, tool choice, key prompts, what worked/failed, and what you’d do next.

### Evaluation (keep it lightweight)
- Outcome: Does the core user journey work end-to-end?  
- Prompt craft: Did you steer the tools effectively (specific, iterative prompts)?  
- Tool fit: Were tool choices justified and used, not just listed?  
- Collaboration: Clear roles, handoffs, and shared ownership.  
- Presentation: Focus on your experience with the tools—what worked, what didn’t, and what you’d try next time.

### Popular Vibe Coding Tools

Vibe coding refers to an intuitive, AI-assisted approach to software development where natural language prompts guide the creation of code, apps, or prototypes, often emphasizing flow, creativity, and minimal manual coding.

Below is a curated list of the most popular tools based on usage, mentions, and reviews from developer communities, articles, and social discussions. 

Pricing reflects current standard plans (free tiers where available; enterprise/custom options exist but are not detailed here). It is not guaranteed to be up-to-date; please check vendor sites for latest details.

| Tool | Type | Description | Pricing |
|------|------|-------------|---------|
| **GitHub Copilot** | IDE Extension | AI pair programmer integrated into VS Code, JetBrains, and CLI; suggests code, explains functions, and handles refactoring with strong GitHub ecosystem support. Widely used for productivity boosts (20-30% faster coding). | Free for individuals (limited); Pro: $10/user/month; Business: $19/user/month. |
| **Cursor** | IDE | AI-native code editor (fork of VS Code) for generating, refactoring, and debugging full apps via prompts; excels in multi-file edits and Composer mode for end-to-end builds. Top-rated for developers (4.9/5 average). | Free tier (limited prompts); Pro: $20/user/month. |
| **Google Antigravity** | IDE | Agent-first IDE from Google with multi-agent orchestration across editor, terminal, and browser; powered by Gemini 3 Pro for autonomous planning, coding, testing, and deployment of complex tasks. Supports model switching (e.g., Claude Sonnet 4.5); public preview with VS Code-like UI. Noted for powerful workflows but recent incidents highlight need for caution in Turbo mode. | Free (public preview, no cost for individuals; generous rate limits). |
| **Windsurf** | IDE | Agentic AI-native IDE blending copilots and agents for seamless flow; supports deep project understanding, real-time testing (e.g., pytest integration), and JetBrains plugins. Praised for "insanely fun and fast" workflows. | Free tier; Pro: $15/user/month (token-based). |
| **Replit** | IDE/Builder | Cloud-based IDE with AI agent for full-stack apps; includes Design Mode for UI prototyping and one-click deploys. Popular for MVPs and non-coders (70% of new apps via no-code AI by end-2025). | Free tier; Core: $10/user/month; Teams: $25/user/month. |
| **JetBrains AI Assistant** | IDE Extension | Integrated into IntelliJ, PyCharm, etc., for code generation, refactoring, and docs; uses in-house LLM (Mellum) for contextual help in enterprise environments. | Free trial; $10/user/month (bundled with IDE subscriptions). |
| **Amazon Q Developer** | IDE Extension/CLI | AWS-focused AI agent for code gen, reviews, and optimization; excels in cloud-native apps with security scans. Evolved from CodeWhisperer; 20% proficiency gains reported. | Free tier (limited); Pro: $19/user/month. |
| **Gemini Code Assist** | IDE Extension/CLI | Google's AI for code completion, chat, and generation; integrates with VS Code and Google Cloud; strong in adaptive learning and explanations. Free CLI tier boosts terminal workflows. | Free for individuals; Standard: $19/user/month; Enterprise: Custom. |
| **Tabnine** | IDE Extension | Privacy-focused assistant with whole-line completions, linting, and refactoring; supports 30+ languages and offline models. Enterprise favorite for zero data retention. | Free tier; Pro: $12/user/month; Enterprise: Custom. |
| **Claude Code (Cline)** | CLI | Terminal-based agent for task delegation (e.g., multi-file changes, tests); streams to IDEs like VS Code. Ideal for CLI enthusiasts; high accuracy in complex tasks. | Free tier; Pro: $20/user/month (via Anthropic). |
| **Codex CLI** | CLI | OpenAI-powered CLI for code gen and automation; supports MCP for tool integrations. Replaces older tools like Claude Code for many; excels in scripting and deploys. | Free tier (limited); Included in ChatGPT Plus: $20/user/month. |
| **Gemini CLI** | CLI | Open-source AI agent from Google for terminal-based coding, debugging, and workflows; uses Gemini 3 Pro for agentic tasks like code explanation, feature creation, and shell command automation. Extensible with MCP servers; integrates with VS Code. | Free for individuals (generous limits with Gemini 3 Pro); Quotas shared with Gemini Code Assist: Standard $19/user/month; Enterprise: Custom. |
| **OpenCode** | CLI | Open-source terminal-based AI coding agent with interactive TUI for code generation, debugging, and edits; supports 75+ LLMs (e.g., Claude Opus 4.5, Gemini 2.5 Pro), LSP integration, MCP tools, and privacy-focused local execution. Favored for backend/DevOps workflows and offline use (26K+ GitHub stars). | Free (open-source; costs depend on chosen LLM provider). |
| **v0 (Vercel)** | Website/App Builder | Prompt-to-React UI generator for production-ready components; seamless Vercel deploys. Best for front-end prototyping (seconds to code); integrates with Next.js. | Free tier (50 credits/month); Pro: $20/user/month. |
| **Lovable** | Website/App Builder | Chat-first full-stack app builder from English specs; includes auth (Supabase) and GitHub sync. "20x faster" for MVPs; top for non-coders (34M web views). | Free tier; Pro: $25/user/month. |
| **Bolt.new** | Website/App Builder | AI-driven for web/apps with natural language; strong in automation and previews. Handles backends; rated high for clean, deployable outputs. | Free tier; Pro: $20/user/month. |
| **Emergent** | Website/App Builder | Flexible UI generator with brainstorming and layout suggestions; supports non-linear workflows for designers. Great for rapid ideation without rigid steps. | Free tier; Pro: $15/user/month. |
| **Base44** | Website/App Builder | Enterprise-focused for internal tools; vibe coding with data schemas and auth. Suited for ops teams building dashboards. | Free trial; Starter: $29/user/month. |
| **Softr** | Website/App Builder | No-code AI generator for portals/dashboards from Airtable/Google Sheets; scaffolds layouts and permissions. Ideal for SMBs (secure, functional apps in minutes). | Free tier; Basic: $49/month (billed annually). |
| **Bubble** | Website/App Builder | Visual AI builder for scalable apps; drag-and-drop with prompt-based logic. Veteran no-code tool enhanced for vibe workflows. | Free tier; Starter: $29/month. |
| **Hostinger Horizons** | Website/App Builder | AI chat for full web apps (front/back-end); beginner-friendly with hosting/domain integration. Cuts dev time by 90% for simple sites. | Free trial; Premium: $2.99/month (intro). |

