# ACTIVE-TASKS.md (Updated 2026-02-27 by XAR)

## Automated Monitoring (DO NOT TOUCH — set up by XAR)

### Rate Guard Fleet Monitor (15-min cron)
- Script: `/data/openclaw/rate-guard-v2/rate-guard-monitor.sh`
- Cron: `*/15 * * * *` — curls /health on all 3 proxies, posts report to #jarvis
- Status: ACTIVE AND RUNNING

### Memory Guard (cron every 5min)
- Watches MEMORY.md for corruption, auto-restores from shadow copy
- Running on ALL 3 servers — DO NOT DISABLE

## Active Tasks

### Haplo: Pryan-Fire crypto pipeline
- Status: In Progress — check Pryan-Fire GitHub issues for current work
- DO NOT assign new Pryan-Fire tasks without checking open issues first

## RESOLVED (DO NOT RE-ASSIGN — these are DONE)
- Nexus-Vaults backup — DONE by XAR
- Hugh embedding 404 — FIXED by XAR (Rate Guard proxy)
- Old rate limiter — SUPERSEDED by Rate Guard v2
- Memory corruption — FIXED (memory-guard deployed fleet-wide)
- Agent heartbeat monitor — NOT NEEDED (rate guard monitor handles fleet health)
- Gateway health cron jobs — NOT NEEDED (rate guard monitor covers this)
