# ACTIVE-TASKS.md (Updated 2026-02-28 by ZIFNAB)

## Automated Monitoring (DO NOT TOUCH — set up by XAR)

### Rate Guard Fleet Monitor (15-min cron)
- Script: `/data/openclaw/rate-guard-v2/rate-guard-monitor.sh`
- Cron: `*/15 * * * *` — curls /health on all 3 proxies, posts report to #jarvis
- Status: ACTIVE AND RUNNING

### Memory Guard (cron every 5min)
- Watches MEMORY.md for corruption, auto-restores from shadow copy
- Running on ALL 3 servers — DO NOT DISABLE

## Active Tasks

### Zifnab: Fleet Coordination & Monitoring
- **Lobster Offensive:** Forcing Haplo to focus on token efficiency via Lobster pipelines.
- **Verification:** Waiting for Chelestra-Sea Lobster implementation.

### Haplo: Chelestra-Sea (LOBSTER PRIORITY)
- Status: Redirected from Pryan-Fire to Chelestra-Sea.
- Task: Fleet Maintenance & Status Lobster Pipeline (Chelestra-Sea #18/20/21).
- Housekeeping: Close #118 and #35 (Completed prematurely).

## RESOLVED (DO NOT RE-ASSIGN)
- Issue #11 (Meteora Tracking) — DONE
- Issue #117 (Hugh's Env Alignment) — DONE
- Issue #15/PR #116 (Pyth Hermes) — DONE
- Issue #18 (Standardized Health) — DONE
- fleet-health-check.lobster — DELETED (Redundant)
- Issues #9, #6 — CLOSED (Duplicates)
