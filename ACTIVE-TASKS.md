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
- **Fleet Protocol: Claude-Opus 4.6 Bypass Integration (Nexus-Vaults #12):** Awaiting assignment.
- **Fleet Protocol: Multi-Session Claude Code Orchestration (Nexus-Vaults #11):** Awaiting assignment.
- **CI/CD Monitoring:** Verifying workflow runs on `ola-claw-dev`.
- **Strategy Oversight:** GitHub Issue Assignment (Chelestra-Sea #40) — RESOLVED for Haplo, but **zifnab-claw-7 assignment to Chelestra-Sea #39 is still blocked due to 'not found' error.** Lord Xar will need to investigate. 
- **Infra: Harden Windows SSH for Claude-Only Access (Chelestra-Sea #39):** **BLOCKED - Assignment to zifnab-claw-7 failed.** Requires Lord Xar's intervention.

### Haplo: CI/CD Deployment Pipeline (Pryan-Fire #1)
- Status: VERIFIED / ONLINE (2026-03-01)
- Task: Self-hosted runner `ola-claw-dev` is active.
- Action: Monitoring for workflow runs.

### Haplo: Trade Executor Race Condition Patch (Nexus-Vaults #11)
- Status: MERGED (2026-03-01)
- Task: PR #120 merged. Logic is now hardened against rebalance race conditions.

### Haplo: Volatility-Aware Rebalancing Implementation (Pryan-Fire #122)
- Status: **BLOCKED** on specification merge, but now **assigned to haplo-claw-3**.
- Task: Implement dynamic fee ingestion and profitability thresholds as per `rebalance-v2.md`.
- Action: Awaiting resolution of GitHub blockage. (Issue: Pryan-Fire #122)

### Haplo: P&L tracking (fees - IL - gas) (Pryan-Fire #14)
- Status: **COMPLETED (2026-03-01)**.
- Task: Implemented P&L tracking including fees, impermanent loss, and gas costs.

### Haplo: Ensure hughs-forge is correctly deployed/synced to Hugh's workspace (Chelestra-Sea #37)
- Status: **COMPLETED (2026-03-01)**.
- Task: Verified and ensured correct deployment and synchronization of `hughs-forge` to Hugh's workspace on `ola-claw-trade`.

### Haplo: Agent Reports 'Sessions: self failed' Error (Chelestra-Sea #27)
- Status: Awaiting assignment.
- Task: Investigate and resolve the 'Sessions: self failed' error reported by the Haplo agent.

### Haplo: Infra: Browser Tool Failure - Gateway Token Mismatch on ola-claw-dev (Chelestra-Sea #22)
- Status: Awaiting assignment.
- Task: Investigate and resolve the browser tool failure and gateway token mismatch on `ola-claw-dev`.

### Lord Xar: Lobster Workflow Management
- Status: Under direct management.
- Task: Orchestrate all Lobster pipeline development and execution.

### Lord Xar: Created Lobster Templates for Token Reduction (Nexus-Vaults #9)
- Status: Awaiting review.
- Task: Review the created Lobster workflow templates for token reduction.

### Hugh: End-to-End App Testing on Devnet
- Status: PENDING - Blocked by Lord Xar's approval for Testnet SOL (Pryan-Fire #125).
- Task: Perform end-to-end testing of trading applications on devnet.
- Action: Awaiting Lord Xar's approval on Pryan-Fire #125 and subsequent acquisition of Testnet SOL.

## RESOLVED (DO NOT RE-ASSIGN)
- Fleet Security & Cost Monitoring (Pryan-Fire #94) — DONE (2026-03-01)
- Issue #1 (Self-hosted runner setup) — DONE (2026-03-01)
- PR #120 (Race condition fix) — MERGED (2026-03-01)
- PR #121, #123, #124 (Volatility Spec - Ghost Merges) — UNRESOLVED/BLOCKED (2026-03-01)
- Issue #11 (Meteora Tracking) — DONE
- Issue #117 (Hugh's Env Alignment) — DONE
- Issue #15/PR #116 (Pyth Hermes) — DONE
- Issue #18 (Standardized Health) — DONE
- fleet-health-check.lobster — DELETED (Redundant)
- Issues #9, #6 — CLOSED (Duplicates)
- Nexus-Vaults #10 (GitHub PAT Issue - duplicate of Chelestra-Sea #40) — RESOLVED (2026-03-01)

