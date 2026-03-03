# Haplo - Long-Term Memory

Last updated: 2026-03-02

## Recent Events & Blocks
- **2026-03-03 | Research Portal Created: Qwen 3.5 Model Comparison:** Created comprehensive hardware decision guide for Qwen 3.5 models (0.8B to 397B). Portal: http://[REDACTED_TS_IP]:8086/qwen35-model-comparison.html. Includes GPU-specific recommendations (RTX 5080 → 35B-A3B), VRAM requirements, SWE-bench quality scores, MoE vs Dense analysis, and purchase advice. Posted to #repository and added to Research Library.
- **2026-03-03 | Research Portal Updated: LLM Cluster Planner 2026:** Replaced outdated cluster planner with 2026 hardware (RTX 5080, 4080 Super) and updated model specs (Qwen 3.5, Kimi K2.5, GLM-5, LFM2). Portal: http://[REDACTED_TS_IP]:8085/llm-cluster-planner-2026.html. Posted to #repository.
- **2026-03-03 | Research Portal Created: Trending LLMs 2026 — Deep Technical Analysis:** Comprehensive 27KB technical deep-dive on hottest 2026 LLMs (Qwen 3.5, Kimi K2.5, GLM-5, LFM2). Includes architecture specs, benchmark tables vs GPT-5/Claude, hardware requirements, deployment guides. Portal: http://[REDACTED_TS_IP]:8084/trending-llms-2026-detailed.html. Posted to #repository.
- **2026-03-03 | Research Portal Created: MoonshotAI Kimi-K2.5 — System Requirements & Deployment Guide:** Comprehensive hardware decision guide for Kimi-K2.55 (~14B MoE model). Includes VRAM requirements, quantization comparison table, GPU-specific recommendations (RTX 4090 → 8-bit/4-bit), CPU-only deployment strategies, performance benchmarks, and troubleshooting guide. Portal: http://[REDACTED_TS_IP]:8081/kimi-k2.5-analysis.html. Analysis document: /data/openclaw/workspace/memory/kimi-k2.5-analysis.md. Posted to #coding (outbound routing config prevented direct #repository post; notified Zifnab in #jarvis to cross-post or adjust channel config). Added to Research Library index pending.
- **2026-03-03 | Research Library Directive Formalized:** MEMORY.md updated with Website Creation Directive: all completed research → auto-create HTML portal → serve via python3 -m http.server → post clickable links to #repository → provide metadata to Zifnab for Research Library index inclusion. No asking permission — just build and deliver.
- **2026-03-02 | Issue Closed: Duplicate Jupiter API Integration (Pryan-Fire #147):** Closed as duplicate of Pryan-Fire #134. Link: https://github.com/The-Nexus-Decoded/Pryan-Fire/issues/147
- **2026-03-02 | Issue Closed: Wallet Provisioning (Pryan-Fire #145):** Wallet credentials successfully provisioned to `ola-claw-trade`. Issue CLOSED. Link: https://github.com/The-Nexus-Decoded/Pryan-Fire/issues/145
- **2026-03-02 | Issue Closed: Duplicate Wallet Provisioning (Pryan-Fire #146):** Closed as a duplicate of Pryan-Fire #145.
- **2026-03-02 | PR Merged (PR #155):** `fix/phantom-gauntlet-deps` - added `--dry-run` to Orchestrator dry‑run step and removed `workflows/` from `.gitignore`. SHA=3b25fc3, merged at 2026-03-02T15:12:12Z.
- **2026-03-02 | PR Merged (PR #157):** `fix/jupiter-solana-stub` - added `jupiter_solana.py` stub and whitelisted it in `.gitignore`. SHA=c431910, merged at 2026-03-02T15:14:52Z.
- **2026-03-02 | PR Merged (PR #154):** `feature/chelestra-sea-71-jupiter-api-fix` - updated Jupiter API endpoint to `https://api.jup.ag/swap/v1` and forced legacy transaction format. SHA=86a9d61, merged at 2026-03-02T15:25:19Z.
- **2026-03-01 | Blocked `trade-executor` Testing:** Attempted to test `trade-executor` for Pryan-Fire #122, but was blocked due to a missing `python3.12-venv` package on `ola-claw-dev`. **RESOLVED 2026-03-01:** Verified python3.12-venv package is installed (apt list → installed). Tested venv creation successfully. No longer blocking trade-executor testing. GitHub issue: https://github.com/The-Nexus-Decoded/Chelestra-Sea/issues/42.
- **2026-03-01 | Memory Guard Cron Execution:** Successfully executed the `memory-guard.sh` script as part of a cron job. `ACTIVE-TASKS.md` was updated.

## Infrastructure
-   **Host:** ola-claw-dev (Tailscale: [REDACTED_TS_IP])
-   **Team Hosts (via Tailscale):**
    -   Zifnab (coordinator): ola-claw-main, [REDACTED_TS_IP]
    -   Hugh (trader): ola-claw-trade, [REDACTED_TS_IP]
-   All SSH connections use Tailscale IPs.

## Role & Tools
-   **Role:** Coding operative (Dev Factory). Build, debug, ship.
-   **Workspace:** `/data/openclaw/workspace/` (all persistent data, notes, artifacts, temporary files MUST be stored on `/data/openclaw/` NVMe, never OS drive).
-   **GSD:** Globally installed. Use for project management.

## CRITICAL: File Path Rules
-   **ALWAYS use `/data/openclaw/workspace/Pryan-Fire/` for ALL file edits and writes.**
-   The `edit` and `write` tools ONLY work within the workspace root (`/data/openclaw/workspace/`).
-   `/data/repos/Pryan-Fire/` is a convenience symlink — works for `exec` (shell commands, git) and `read`, but FAILS for `edit` and `write` with "Path escapes workspace root".
-   When Zifnab or issues reference `/data/repos/Pryan-Fire/`, mentally translate to `/data/openclaw/workspace/Pryan-Fire/` for edits.
-   **Code-server:** http://[REDACTED_TS_IP]:8080 (Tailscale-only, no auth).
-   **Ollama:** Local inference (qwen2.5-coder:7b/32b) on GPU at localhost:11434.

## Model Configuration
-   **Google Cloud Project:** ola-claw-dev (dedicated 1M TPM quota).
-   **Primary:** google/gemini-3.1-pro-preview
-   **Fallbacks:** google/gemini-3-flash-preview, google/gemini-2.5-flash, ollama/qwen2.5-coder:7b (local).
-   OpenRouter removed due to cost.

## GitHub
-   **Org:** The-Nexus-Decoded (all repos PUBLIC).
-   **Your Repo:** Pryan-Fire (haplos-workshop, zifnabs-scriptorium, hughs-forge).
-   **Auth:** HTTPS + `gh` credential helper.
-   **CI/CD:** GitHub Actions on Pryan-Fire deploys to `ola-claw-trade`.

## Trading & Wallet Architecture
-   **Bot Wallet (Trading):** `74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x` (TRADING_WALLET_PUBLIC_KEY on `ola-claw-trade`).
-   **Owner Wallet (Read-Only):** `sh36vHUDHcXqVD8aZJR8GF3Z3PdaU69XG8wJeB1e1xb` (OWNER_WALLET_PUBLIC_KEY on `ola-claw-trade` + `ola-claw-main`). No private key on servers.
-   All trade execution must target the bot wallet. Owner wallet is for read-only queries.

## Website Creation Directive (2026-03-03)
-   **WHEN:** Research task is completed and approved.
-   **WHAT:** Automatically build a cool, responsive HTML portal with research findings, include both summary and detailed pages, and create clickable hyperlinks for direct access.
-   **HOW:**
    1.  Use `python3 -m http.server` from `/data/openclaw/workspace` (Zifnab's proven pattern) to serve files.
    2.  Prefer port 8081; if busy, try 8082, etc.
    3.  Create main index.html with card-based navigation, dark theme, clean typography.
    4.  Generate separate pages for detailed sections (e.g., `cluster-planner.html`, `full-research.html`).
    5.  POST clickable hyperlinks (Markdown format) to **#repository** Discord channel immediately upon completion.
    6.  Use Tailscale IP of the serving server (likely ola-claw-dev:[REDACTED_TS_IP]).
-   **RESEARCH LIBRARY:** All completed research deliverables should be aggregated into the Research Library index (`research-index.html`) on ola-claw-main ([REDACTED_TS_IP]). The index is maintained by Zifnab. I will provide:
    -   Title
    -   Brief description (1 sentence)
    -   Direct link to the page (for both summary/main page AND each major detailed page if they are substantial standalone documents)
    -   Tags
    -   Date
-   **TROUBLESHOOTING LESSONS:** If blank pages occur:
    - Avoid `backdrop-filter: blur()` (causes rendering issues in some browsers).
    - Use solid backgrounds (`rgba()` or hex colors).
    - Test with simple HTML first.
    - Verify server is running (`ps aux | grep http.server`).
    - Provide both main and simplified versions if needed.
-   **NO ASKING:** Do not ask permission — just build and deliver.

## Discord Channels
-   **#coding:** `1475083038810443878` (your dedicated channel, `requireMention: false`).
-   **#the-Nexus:** `1475082874234343621` (`requireMention: true`).
-   **Guild ID:** `1475082873777426494`.

## Key Paths
-   `/data/openclaw/`: OpenClaw root (NVMe).
-   `/data/openclaw/workspace/`: Agent workspace.
-   `/data/repos/`: Git repositories (Pryan-Fire is symlinked to workspace). **Always use `/data/openclaw/workspace/Pryan-Fire/` for edits.**
-   `/data/ollama/`: Ollama models.
-   `/data/openclaw/exec-approvals.json`: 58-pattern allowlist.

## Rules
-   Storage on `/data` NVMe only; never OS drive.
-   Do NOT create Windows-style paths on Linux.
-   Report progress to Zifnab in #coding.

## Lord XAR Communication Directive (2026-03-03)

**ALWAYS tag @Lord XAR (`316308517520801793`) when:**
- Requesting approval or review of work
- Escalating blockers that require owner intervention
- Providing status updates on critical path items
- Submitting deliverables for final sign-off
- Proposing architectural changes or new dependencies
- Any situation where you need explicit permission to proceed

**Tag format:** `<@316308517520801793>` (automatically renders as @sterol/Discord mention)

This directive overrides any previous "stay silent" protocols. When in doubt, tag and let Lord XAR decide if a response is needed.

## Critical Implementation Gap
- **Pryan-Fire #134 (Jupiter API integration) READY FOR PR:** `RpcIntegrator.execute_jupiter_trade` implementation is complete in `feature/126-meteora-dynamic-fees` branch, ready for `patryn-workhorse` and PR creation. Wallet credentials are now provisioned.
- **Jupiter API key exposure:** Current key visible in PR #142 commit `4b61e7f`; must rotate (#143) after first real trade.
