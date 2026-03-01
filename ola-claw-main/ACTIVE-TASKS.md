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
- [x] Claude Code Analysis (Nexus-Vaults #11) - Zifnab - Completed deep-scan of `hughs-forge/services/trade-executor/main.py`. Findings logged.
- [ ] Implement Trade-Executor Fixes (Nexus-Vaults #12) - Haplo - Addressing security (hardcoded keys), RPC retry logic, and strategy stubs found in analysis.
- [ ] Fleet Workspace Git Sync (Nexus-Vaults#1) - Zifnab - Ongoing daily redaction and push to GitHub.

### Zifnab: Fleet Coordination & Monitoring
- **Claude Analysis:** Monitoring progress of current analysis. Will intervene if stalled.
- **Lobster Workflows:** Delegated to Lord Xar for direct management.
- **Verification:** Continuous monitoring of Rate Guard budgets.

### Haplo: CI/CD Deployment Pipeline (Pryan-Fire #1)
- Status: ACTIVE (2026-03-01)
- Task: Unblock via self-hosted runner on `ola-claw-dev`.
- Action: Haplo executing.

### Haplo: Claude Code Integration & Verification (Nexus-Vaults #11)
- Status: Ready for Claude Code analysis and report integration.
- Task: Implement local integration and verification patterns for Claude Code analysis.
- Action: Await Claude Code analysis results for `hughs-forge/services/trade-executor/main.py` from Zifnab.

### Lord Xar: Lobster Workflow Management
- Status: Under direct management.
- Task: Orchestrate all Lobster pipeline development and execution.

## RESOLVED (DO NOT RE-ASSIGN)
- Fleet Security & Cost Monitoring (Pryan-Fire #94) — DONE (2026-03-01)
- Issue #11 (Meteora Tracking) — DONE
- Issue #117 (Hugh's Env Alignment) — DONE
- Issue #15/PR #116 (Pyth Hermes) — DONE
- Issue #18 (Standardized Health) — DONE
- fleet-health-check.lobster — DELETED (Redundant)
- Issues #9, #6 — CLOSED (Duplicates)
