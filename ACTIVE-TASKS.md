# ACTIVE-TASKS.md (Updated 2026-03-01 by ZIFNAB)

## Automated Monitoring (DO NOT TOUCH — set up by XAR)

### Rate Guard Fleet Monitor (15-min cron)
- Script: `/data/openclaw/rate-guard-v2/rate-guard-monitor.sh`
- Cron: `*/15 * * * *` — curls /health on all 3 proxies, posts report to #jarvis
- Status: ACTIVE AND RUNNING

### Memory Guard (cron every 5min)
- Watches MEMORY.md for corruption, auto-restores from shadow copy
- Running on ALL 3 servers — DO NOT DISABLE

## Active Tasks

- [x] Claude Code & Build Workflow Integration (Nexus-Vaults #11) - Haplo - Pattern verified and ready for delegation.
- [x] Pryan-Fire Windows Clone (Nexus-Vaults #11 related) - Zifnab - `Pryan-Fire` repository successfully cloned to `C:\Users\olawal\Pryan-Fire` on Windows workstation.
- [x] Claude Code Analysis (Nexus-Vaults #11) - Zifnab - Completed initial analysis; identified race condition.
- [ ] Fleet Workspace Git Sync (Nexus-Vaults#1) - Zifnab - Ongoing daily redaction and push to GitHub.
- [ ] Security: PAT exposed in channel - rotation required (Chelestra-Sea #43) - Zifnab (PAT rotation pending GitHub unblock), Haplo (local verification)

### Zifnab: Fleet Coordination & Monitoring
- **Rate Guard Fleet Monitor:** Active (15-min cron).
- **Memory Guard:** Active (5-min cron).
- **GitHub Operations:** Currently blocked from merging/closing PRs on Pryan-Fire due to token permissions (infection flagged by GitHub). Escalated to Lord Xar.
- **Trading Pipeline Bugfixes (Pryan-Fire #133–#139):** In Progress. Implemented:
  - TradeExecutor: config-driven paper mode, fail-fast wallet loading (issues #136, #139)
  - Jupiter swap execution via direct HTTP (issue #134)
  - Signal ingestion endpoint on orchestrator (issue #138)
  - Pyth price fallback to CoinGecko (> $1k) likely resolves #137 (verify)
  - Updated RpcIntegrator callers? (RpcIntegrator itself still stub; note: active service uses TradeOrchestrator, not RpcIntegrator)
  - Next: Deploy changes to ola-claw-trade, install missing deps (FastAPI, uvicorn) in orchestrator venv, set env vars for live wallet, test end-to-end.
- **Service Integration:** Modified TradeOrchestrator to embed TradeExecutor and start HTTP signal server (port 8002). Need to verify dependencies and restart service.

### Haplo: CI/CD Deployment Pipeline (Pryan-Fire #1)
- Status: **BLOCKED** - Self-hosted runner `ola-claw-dev` token expired/signature invalid; GitHub Actions jobs stuck in queued.
- Action: Re-register runner with fresh token.
- Impact: Blocks deployments (PR #132 already merged, but not yet deployed).

### Hugh: Chelestra-Sea #2 (Profile Distillation)
- Status: **BLOCKED** - Pending dependency installation (sqlite3, chromadb, PyPDF2, python-docx, openpyxl) requested 2026-03-01.
- Role: Trading operative; will test trading pipeline once Zifnab's fixes are deployed.

### Lord Xar: Lobster Workflow Management
- Under direct management.

## RESOLVED (DO NOT RE-ASSIGN)
- Fleet Security & Cost Monitoring (Pryan-Fire #94) — DONE (2026-03-01)
- Issue #1 (Self-hosted runner setup) — DONE (2026-03-01)
- PR #120 (Race condition fix) — MERGED (2026-03-01)
- PR #132 (Volatility-Aware Rebalancing Implementation) — MERGED (2026-03-01 23:34)
- Pryan-Fire #122 (Volatility-Aware Rebalancing) — DEPLOYED (2026-03-01)
- Pryan-Fire #125 (Devnet Testing Approval) — CLOSED (2026-03-01)
- Nexus-Vaults #10 (GitHub auth issue) — RESOLVED (2026-03-01)
- Chelestra-Sea #34, #35, #48 — CLOSED (2026-03-01)
- Issue #11 (Meteora Tracking) — DONE
- Issue #117 (Hugh's Env Alignment) — DONE
- Issue #15/PR #116 (Pyth Hermes) — DONE
- Issue #18 (Standardized Health) — DONE
- fleet-health-check.lobster — DELETED (Redundant)
- Issues #9, #6 — CLOSED (Duplicates)

