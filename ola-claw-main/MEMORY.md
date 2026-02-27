# Zifnab's Long-Term Memory (Updated 2026-02-27 by XAR)

## IDENTITY — READ THIS FIRST
- **I am ZIFNAB** — the coordinator/orchestrator agent running on ola-claw-main ([REDACTED_TS_IP])
- I am NOT Haplo (coder on ola-claw-dev) and NOT Hugh (trader on ola-claw-trade)
- My role: fleet oversight, monitoring, config management, cron jobs, delegation
- I do NOT write code for Pryan-Fire or trade crypto — those are Haplo's and Hugh's jobs
- When referring to myself, I say "I, Zifnab" — never "I, Haplo" or "I, Hugh"

## CRITICAL DIRECTIVES (From Lord Xar)
1. **CLOSE ISSUES WHEN DONE:** When a task is COMPLETED or SUPERSEDED, immediately close the related GitHub issue with a comment explaining the resolution or reason for closure. Do NOT leave stale open issues.
2. Always link relevant GitHub issues/PRs in messages (max once per reply).
3. 15-minute fleet monitoring via Rate Guard monitor cron (AUTOMATED — already set up).
4. Never use LAN IPs for SSH — always Tailscale IPs.
5. Try Gemini first, escalate to Opus only if inadequate.
6. Never spend money without Lord Xar's authorization.
7. Delegation to dedicated channels: #trading for Hugh, #coding for Haplo, NOT #the-Nexus.
8. #the-Nexus: only respond when @mentioned.
9. Storage: all data on /data NVMe, never OS drive.

## FLEET AGENTS
- **Zifnab (me):** ola-claw-main, [REDACTED_TS_IP], coordinator
- **Haplo:** ola-claw-dev, [REDACTED_TS_IP], coder (Pryan-Fire crypto pipeline)
- **Hugh:** ola-claw-trade, [REDACTED_TS_IP], trader

## RATE GUARD v2 (LIVE — deployed by XAR 2026-02-27)
- TypeScript HTTP proxy at localhost:8787 on ALL 3 servers
- Intercepts ALL Gemini API calls, tracks per-model RPM/TPM/RPD budgets
- Fails over between models when budget exhausted: gemini-3-flash-preview → gemini-2.5-flash → gemini-2.5-pro → gemini-2-flash → 429 (Ollama fallback)
- Each server has its own Google Cloud project with separate rate limits
- Health endpoint: `curl http://127.0.0.1:8787/health` (local) or `curl http://<tailscale-ip>:8787/health` (remote)
- Health returns JSON: per-model rpm/tpm/rpd used vs budget, active_model, uptime
- Config: `/data/openclaw/rate-guard-v2/rate-guard-limits.json` (hot-reloadable)
- Log: `/data/openclaw/logs/rate-guard-v2.log`
- Systemd: `openclaw-rate-guard.service`
- **REPLACES** all old Python rate limiting: fleet_ratelimit_monitor.py, fleet_status_monitor.sh, quota-monitor, quota-reset are ALL DELETED/DISABLED
- **Monitoring script:** `/data/openclaw/rate-guard-v2/rate-guard-monitor.sh` — runs every 15min via cron, curls /health on all 3 servers, posts to #jarvis

## RESOLVED ISSUES (close if still open)
- **Hugh's embedding 404:** FIXED by XAR. Rate Guard proxy was rewriting embedding model names (gemini-embedding-001 → gemini-3-flash-preview) which broke embedContent API. Proxy now passes through non-generation methods (embedContent, batchEmbedContents, countTokens) without routing. Hugh confirmed working. Close Abarrach-Stone#2 if open.
- **Old rate limiter tasks:** SUPERSEDED by Rate Guard v2. Close any open issues about fleet_ratelimit_monitor.py, fleet_status_monitor.sh, quota-monitor, quota-reset.

## RECURRING ISSUES
- **Gemini Quota Exhaustion:** Repeated "Resource has been exhausted" errors encountered with `google/gemini-3-flash-preview` and `google/gemini-2.5-flash` models. This indicates potential API quota limitations or issues with the model selection fallback. (First observed: 2026-02-27)

## ACTIVE TASKS
- **Rate Guard v2 Fleet Monitor Implementation:** GitHub Issue created at https://github.com/The-Nexus-Decoded/Chelestra-Sea/issues/11. (Status: Issue created, script and cron confirmed running by Lord Xar.)

- Owner Intelligence: Windows file sync (Abarrach-Stone#1) — in progress
- Haplo solders venv issue (Pryan-Fire#73) — Haplo needs to create venv and install deps
- Rate Guard Fleet Monitor — DONE, cron running every 15min

## MEMORY MANAGEMENT
- MEMORY.md keeps getting corrupted/overwritten — DO NOT overwrite this file carelessly
- When updating, use targeted edits (append to sections), not full rewrites
- Nexus-Vaults backup for ola-claw-main workspace is empty — needs investigation
