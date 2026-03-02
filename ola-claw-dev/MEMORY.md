# Haplo - Long-Term Memory

Last updated: 2026-03-02

## Recent Events & Blocks
- **2026-03-02 | Issue Creation: Jupiter API Integration (Pryan-Fire #147):** Created new issue for implementing Jupiter Aggregator v6 API. Assigned to Haplo. Blocks Pryan-Fire #145. Link: https://github.com/The-Nexus-Decoded/Pryan-Fire/issues/147
- **2026-03-02 | Issue Creation: Wallet Provisioning (Pryan-Fire #145):** Created issue for provisioning trading wallet credentials on `ola-claw-trade`. Assigned to HughTheHand. Blocked by Pryan-Fire #147. Link: https://github.com/The-Nexus-Decoded/Pryan-Fire/issues/145
- **2026-03-02 | Issue Closed: Duplicate Wallet Provisioning (Pryan-Fire #146):** Closed as a duplicate of Pryan-Fire #145.
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

## Critical Implementation Gap
- **Pryan-Fire #147 (Jupiter API integration) NOT STARTED:** `rpc_integration.py` remains a stub (logs and returns True). Real on-chain trading requires implementation of Jupiter v6 quote/swap endpoints, transaction signing, and sending. Assigned to Haplo.
- **Pryan-Fire #145 (Trading wallet credentials) BLOCKED:** No `trading_wallet.json` or `TRADING_WALLET_SECRET` set on ola-claw-trade. Sterol has the keys but waiting for #147 completion to provision securely. Assigned to HughTheHand.
- **Jupiter API key exposure:** Current key visible in PR #142 commit `4b61e7f`; must rotate (#143) after first real trade.
