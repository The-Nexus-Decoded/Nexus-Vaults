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

### Zifnab: Fleet Coordination & Monitoring
- **CI/CD Monitoring:** Verifying first workflow runs on `ola-claw-dev` for PR #120.
- **Strategy Oversight:** Finalizing review of `rebalance-v2.md` spec.

### Haplo: CI/CD Deployment Pipeline (Pryan-Fire #1)
- Status: VERIFIED / ONLINE (2026-03-01)
- Task: Self-hosted runner `ola-claw-dev` is active.
- Action: Monitoring for first production workflow run.

### Haplo: Trade Executor Race Condition Patch (Nexus-Vaults #11)
- Status: MERGED (2026-03-01)
- Task: PR #120 merged. Proceeding to deployment verification after CI/CD.

### Haplo: Volatility-Aware Rebalancing Spec (Pryan-Fire #122)
- Status: COMMITTING SPEC (2026-03-01)
- Task: Finalize documentation in `rebalance-v2.md`.
- Action: Haplo pushing to `feature/volatility-rebalance-spec`.

### Lord Xar: Lobster Workflow Management
- Status: Under direct management.
- Task: Orchestrate all Lobster pipeline development and execution.

## RESOLVED (DO NOT RE-ASSIGN)
- Fleet Security & Cost Monitoring (Pryan-Fire #94) — DONE (2026-03-01)
- Issue #1 (Self-hosted runner setup) — DONE (2026-03-01)
- PR #120 (Race condition fix) — MERGED (2026-03-01)
- Issue #11 (Meteora Tracking) — DONE
- Issue #117 (Hugh's Env Alignment) — DONE
- Issue #15/PR #116 (Pyth Hermes) — DONE
- Issue #18 (Standardized Health) — DONE
- fleet-health-check.lobster — DELETED (Redundant)
- Issues #9, #6 — CLOSED (Duplicates)
