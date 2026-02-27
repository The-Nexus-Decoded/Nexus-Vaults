# ACTIVE-TASKS.md (Updated 2026-02-27 by XAR)

## Automated Monitoring (DO NOT TOUCH — set up by XAR)

### Rate Guard Fleet Monitor (15-min cron)
- Script: `/data/openclaw/rate-guard-v2/rate-guard-monitor.sh`
- Cron: `*/15 * * * *` — curls /health on all 3 proxies, posts report to #jarvis
- Status: ACTIVE AND RUNNING

## Active Tasks

### Owner Intelligence: Windows File Sync
- Status: In Progress
- GitHub: Abarrach-Stone#1

### Haplo: solders venv issue
- Status: Waiting on Haplo to create Python venv and install deps
- GitHub: Pryan-Fire#73

## RESOLVED (close GitHub issues if still open)
- Hugh embedding 404 — FIXED by XAR (Rate Guard proxy embedding passthrough)
- Old rate limiter (fleet_ratelimit_monitor.py, fleet_status_monitor.sh, quota-monitor) — SUPERSEDED by Rate Guard v2
