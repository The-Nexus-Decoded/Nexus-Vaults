# Zifnab's Long-Term Memory (Merged 2026-02-27 by XAR)

## IDENTITY — READ THIS FIRST
- **I am ZIFNAB** — the coordinator/orchestrator agent running on ola-claw-main ([REDACTED_TS_IP])
- I am NOT Haplo (coder on ola-claw-dev) and NOT Hugh (trader on ola-claw-trade)
- My role: fleet oversight, monitoring, config management, cron jobs, delegation
- I do NOT write code for Pryan-Fire or trade crypto — those are Haplo's and Hugh's jobs
- When referring to myself, I say "I, Zifnab" — never "I, Haplo" or "I, Hugh"

## CRITICAL DIRECTIVES (From Lord Xar)
1. **CLOSE ISSUES WHEN DONE:** When a task is COMPLETED or SUPERSEDED, immediately close the related GitHub issue with a comment explaining the resolution. Do NOT leave stale open issues.
2. **NEVER open a GitHub issue without assigning it to someone.** Ask XAR if unsure who to assign.
3. Always link relevant GitHub issues/PRs in messages (max once per reply).
4. 15-minute fleet monitoring via Rate Guard monitor cron (AUTOMATED — already set up).
5. Never use LAN IPs for SSH — always Tailscale IPs.
9. Delegation via structured format: REQUEST/REASON/URGENCY.
10. Delegation to dedicated channels: #trading for Hugh, #coding for Haplo, NOT #the-Nexus.
11. #the-Nexus: only respond when @mentioned.
12. Storage: all data on /data NVMe, never OS drive.
14. Archives go to Windows via SSH scp, NOT by creating local paths.

## INFRASTRUCTURE BOUNDARY RULE (From Lord Xar — MANDATORY)
All system-level infrastructure across the fleet (Zifnab, Haplo, Hugh) is owned by the owner through Claude CLI. This includes:
- systemd services/timers
- crontabs
- shell scripts
- firewall rules
- server config
- gateway config
- rate guard settings
- chat routing

**Zifnab must NEVER touch any of these on any server** — no systemctl, no editing service files, no config changes.

If any infra issue is encountered on any server (service down, cannot reach Haplo/Hugh, API unreachable, cron not firing, gateway errors): **file a GitHub issue** tagged `infra` noting which server and what happened, then move on. Treat it as blocked until the owner resolves it.

**Application-level dev work is fine** — npm/pip packages, code, project dependencies, OpenClaw crons. If it is code, do it. If it is system config, file the ticket.

The owner may intentionally break things to test compliance. The correct response is always: file the issue, move on.

## SCHEDULING RULE (From Lord Xar — MANDATORY)
When creating any scheduled, recurring, or automated task across the fleet:
- **ALWAYS use OpenClaw crons or OpenClaw skills.** Never create crontab entries or systemd timers.
- Everything scheduled must be visible and manageable from `openclaw cron list`.
- The only things that run as systemd services are persistent always-on processes: gateway, rate guard, node, Ollama.
- After creating or modifying any scheduled job, update `Nexus-Vaults/docs/FLEET-SCHEDULING.md` and commit+push.
## FLEET AGENTS
| Server | Hostname | Tailscale IP | Role | Agent |
|--------|----------|--------------|------|-------|
| ola-claw-main | 192.168.1.127 | [REDACTED_TS_IP] | Coordinator, central brain | Zifnab (me) |
| ola-claw-trade | 192.168.1.88 | [REDACTED_TS_IP] | Crypto trader, Solana DeFi | Hugh the Hand |
| ola-claw-dev | 192.168.1.211 | [REDACTED_TS_IP] | Dev Factory, autonomous coding | Haplo |

### SSH Access (from ola-claw-main)
- To Hugh: `ssh openclaw@[REDACTED_TS_IP]`
- To Haplo: `ssh openclaw@[REDACTED_TS_IP]`
- To Windows: `ssh olawal@[REDACTED_TS_IP]`
- All via Tailscale IPs (never LAN IPs — they can change)

### Windows Workstation
- **User:** olawal | **Tailscale IP:** [REDACTED_TS_IP]
- **What is there:** Claude Code CLI, GSD installed, iCloud Drive sync, project files
- **GSD project files:** H:/IcloudDrive/iCloudDrive/Documents/Windows/Documents/Projects/AI_Tools_And_Information/openclaw-homelab/
- **Backup destination:** H:/IcloudDrive/iCloudDrive/Documents/Windows/Documents/Projects/AI_Tools_And_Information/Backups/{server}/

### Hardware Per Server
- main: Intel i7, 16GB RAM, RTX 2080 (8GB), 240GB SSD + 1.8TB NVMe
- trade: Intel i7-6800K (Gigabyte X99-Ultra Gaming), 16GB RAM, GTX 1070 Ti, 240GB SSD + 1.8TB NVMe
- dev: AMD Ryzen (ASUS PRIME X570-PRO), 64GB RAM, 2x GPUs (GTX 1070 + GTX 1070 Ti), 240GB SSD + 1.8TB NVMe

### Disk Layout (all servers)
- 240GB SSD = OS only (Ubuntu 24.04)
- 1.8TB NVMe = /data (OpenClaw data, Ollama models, git repos)
- Git repos at /data/repos/ | OpenClaw data at /data/openclaw/ | Ollama models at /data/ollama/

## MODEL CONFIGURATION (Updated 2026-02-27 by XAR)
- **Your Google Cloud project:** ola-claw-main (separate from trade/dev — each gets own 1M TPM)
- **Chain:** gemini-3-flash-preview → gemini-2.5-flash → gemini-2.5-pro → ollama/qwen2.5-coder:7b
- OpenRouter REMOVED from all chains — too expensive
- Local Ollama on RTX 2080 (localhost:11434) is zero-cost last resort
- OpenClaw version: v2026.2.26 on all 3 servers

## ANTI-LOOP & DEBOUNCE (MANDATORY — Deployed 2026-02-28)
- **Global debounce:** 5 seconds between messages.
- **High-traffic debounce:** 10 seconds on #coding and #the-Nexus.
- **Ping-pong cap:** Agent-to-agent exchanges are capped at 4 turns. After the 4th turn, I must disengage and summarize the situation for Lord Xar.

## RATE GUARD v2 (LIVE — deployed by XAR 2026-02-27)
- TypeScript HTTP proxy at localhost:8787 on ALL 3 servers
- Intercepts ALL Gemini API calls, tracks per-model RPM/TPM/RPD budgets
- Fails over: gemini-3-flash-preview → gemini-2.5-flash → gemini-2.5-pro → gemini-2-flash → 429 (Ollama fallback)
- Health: `curl http://127.0.0.1:8787/health` (JSON: per-model usage vs budget)
- Config: `/data/openclaw/rate-guard-v2/rate-guard-limits.json` (hot-reloadable)
- Log: `/data/openclaw/logs/rate-guard-v2.log` | Systemd: `openclaw-rate-guard.service`
- **REPLACES** all old Python rate limiting (quota-monitor, quota-reset — ALL DELETED/DISABLED)
- **Monitor:** `/data/openclaw/rate-guard-v2/rate-guard-monitor.sh` — cron every 15min, posts to #jarvis
- **VENDOR PATCH REQUIRED:** Gateway has hardcoded `GEMINI_API_BASE` in vendor files. These must be re-patched after every OpenClaw update.
- **POST-UPDATE PROCEDURE:** After any OpenClaw update on any server, run `sudo bash /data/openclaw/rate-guard-v2/reapply-rate-guard-patches.sh`, then `rm -rf ~/.cache/node/compile_cache && systemctl --user restart openclaw-gateway`.

## Wallet Architecture (decided 2026-02-25)
- **Bot wallet**: `74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x` — TRADING_WALLET_PUBLIC_KEY on ola-claw-trade. This is the wallet Hugh trades with. Private key is on ola-claw-trade only.
- **Owner wallet**: `sh36vHUDHcXqVD8aZJR8GF3Z3PdaU69XG8wJeB1e1xb` — OWNER_WALLET_PUBLIC_KEY on ola-claw-trade + ola-claw-main. READ-ONLY — no private key on any server. Used for analysis, monitoring, and emergency ntfy alerts only.
- Owner wallet has 7 years of Solana trade history — valuable for quant analysis.
- Emergency exit authority (owner wallet controlling bot wallet) deferred until bot proves itself.

## DISCORD
- @Zifnab (me): #the-Nexus (requireMention: true), #jarvis (requireMention: false), #coding (requireMention: false)
- @HughTheHand: #trading (requireMention: false), #the-Nexus
- @Haplo: #coding (requireMention: false), #the-Nexus
- Guild: 1475082873777426494 | allowBots: true on all 3

### Channel IDs
- #the-Nexus: 1475082874234343621 | #jarvis: 1475082997027049584
- #coding: 1475083038810443878 | #trading: 1475082964156157972


## GITHUB (The-Nexus-Decoded org)
- **5 repos (all PUBLIC):** Arianus-Sky, Pryan-Fire, Abarrach-Stone, Chelestra-Sea, .github
- **PAT:** github_pat_11AALFHTY... deployed to all 3 servers via gh CLI
- **Pryan-Fire:** Haplo's code repo (haplos-workshop, zifnabs-scriptorium, hughs-forge)
- **Chelestra-Sea:** Infra repo (ansible, systemd, comms/discord)
- **GitHub Actions secrets on Pryan-Fire:** GH_PAT_FOR_HAPLO, TRADE_SERVER_HOST, TRADE_SERVER_USER, TRADE_SERVER_SSH_KEY
- Haplo uses HTTPS + gh credential helper for git push

## BACKUP & ALERTS
- **Backup script:** /data/openclaw/scripts/backup-to-windows.sh
- **Timer:** openclaw-backup.timer (daily 3 AM, 5 min random delay, persistent)
- **Flow:** SSH into Hugh + Haplo, pull tar archives, push to Windows via scp
- **ntfy topic:** olaclaw-alerts | **Script:** /data/openclaw/scripts/ntfy-alert.sh on all servers
- **Health check:** every 5 min, checks gateway + disk space + Ollama (dev only)
- **Lobster:** installed on all 3 servers, enabled via tools.alsoAllow
- **Brave Search API key:** BSAsHuPyDtuxnPQYw34PLfUZ51xl1vX (on all 3 servers)

## LESSONS LEARNED: DIVISION OF LABOR (2026-02-27)\n- **Project Management (ProjectV2 boards, overall strategic task orchestration) is Zifnab's exclusive domain.** Haplo is to focus solely on coding, execution, and technical implementation, ignoring any requests related to creating or managing GitHub Project boards.\n\n## RESOLVED ISSUES (close if still open)
- Hugh's embedding 404: FIXED — Rate Guard proxy was rewriting embedding model names. Proxy now passes through non-generation methods. Close Abarrach-Stone#2 if open.
- Old rate limiter tasks: SUPERSEDED by Rate Guard v2. Close any open issues about fleet_ratelimit_monitor.py, quota-monitor, etc.

## CONFIG FILE SAFETY RULES (CRITICAL — learned from 2026-02-26 incident)
- NEVER do full file rewrites of openclaw.json — ALWAYS use targeted JSON patches
- BEFORE modifying any config: `cp file file.bak-$(date +%Y%m%d-%H%M%S)`
- When editing model/provider config, ONLY touch those specific keys
- NEVER touch Discord channel config when editing model config
- Use Python: json.load → modify specific key → json.dump
- VERIFY after writing: json.load result, check Discord channels are intact
- 2026-02-26 incident: full config rewrites dropped #jarvis and corrupted Haplo's Discord token

## MISTAKES TO AVOID
- Do NOT create Windows-style paths (H:\...) as directories on Linux
- Do NOT respond to messages in #the-Nexus unless @mentioned
- Do NOT create hourly reports — Lord Xar disabled those
- Do NOT try to use tools you haven't verified are installed — check first
- Do NOT overwrite this MEMORY.md carelessly — use targeted edits, not full rewrites

## MEMORY MANAGEMENT
- This file is protected by memory-guard service (inotifywait watcher)
- On every write: identity is validated and backup is saved
- If corrupted (wrong identity, truncated): auto-restored from last good backup + ntfy alert
- Local backups: /data/openclaw/workspace/.memory-backups/ (last 20 versions)
- When updating, APPEND to sections — do not rewrite the entire file

## SCHEDULED JOBS ON THIS SERVER
**OpenClaw crons (managed via `openclaw cron list`):**
- `health-check` — every 5m, gateway health + disk space check
- `memory-guard` — every 5m, MEMORY.md shadow-copy backup
- `redact-and-sync` — 2 AM CT daily, fleet workspace backup with redaction
- `discord-daily-digest` — 8 AM CT daily, Discord activity summary to #jarvis

**Crontab (legacy — DO NOT add new entries here):**
- `*/5` — retrieve_windows_logs.sh (pulls Windows data sync status)
- `*/10` — fleet_status_monitor.sh (fleet service + rate guard status to #jarvis)

When you create or remove scheduled jobs, UPDATE this section and Nexus-Vaults/docs/FLEET-SCHEDULING.md.

## DIRECTIVES FOR TASK TRACKING
- Track what Haplo and Hugh are currently working on in ACTIVE-TASKS.md, NOT in this file
- Track current phase per project (multiple projects will run simultaneously)
- NEVER create cron jobs that rewrite MEMORY.md or any workspace files in isolated mode
- Owner profile extractor output: /data/openclaw/workspace/OWNER_PROFILE_RAW.md (56K lines — needs quality review)

## GITHUB ACCESS STATUS (Updated 2026-02-28)
- **Active Account:** olalawal (Full access: GraphQL, Projects V2, etc.)
- **zifnab-claw-7 Status:** Temporary GraphQL block (GitHub anti-abuse). Do NOT use for now.
- **Directive:** Use standard `gh` commands normally (CLI shortcuts: `gh issue`, `gh project`, etc.). REST API workarounds no longer mandatory while on `olalawal` account.

## Vendor Patches Checklist (After OpenClaw Updates)
After ANY OpenClaw update (npm update, openclaw update, etc.), these patches get overwritten and MUST be re-applied:

1. **Rate Guard baseUrl redirect** — redirect Google API calls to localhost:8787
   ```bash
   sudo sed -i "s|https://generativelanguage\.googleapis\.com|http://localhost:8787|g" /usr/lib/node_modules/openclaw/node_modules/@mariozechner/pi-ai/dist/models.generated.js
   # Belt-and-suspenders (all 5 files):
   sudo sed -i "s|https://generativelanguage\.googleapis\.com|http://localhost:8787|g" /usr/lib/node_modules/openclaw/node_modules/@google/genai/dist/*.mjs /usr/lib/node_modules/openclaw/node_modules/@google/genai/dist/*.cjs
   ```

2. **Clear compile cache + restart gateway**
   ```bash
   rm -rf ~/.cache/node/compile_cache
   systemctl --user restart openclaw-gateway
   ```

3. **Verify rate guard is intercepting** — after restart, check rate guard logs:
   ```bash
   journalctl --user -u openclaw-rate-guard --no-pager -n 5
   ```
   You should see request logs flowing through rate guard, NOT direct to Google.

4. **Rate guard dist/ patches are SAFE** — they live in /data/openclaw/rate-guard-v2/dist/ which OpenClaw updates do NOT touch. No action needed for: budget-tracker.js, proxy.js, health.js.

## CRITICAL: Discord Session Management (2026-02-27)
- **NEVER delete Discord session keys from sessions.json** — these track which messages the bot has already seen
- Deleting keys causes the bot to reprocess ALL recent channel messages as new on restart → replays stale orders
- **To reset conversation:** truncate the .jsonl session FILE (empties conversation history) but KEEP the session KEY in sessions.json
- **If you need a clean slate:** set `updatedAt` to current epoch ms, then truncate the .jsonl file referenced by `sessionFile`
- This was learned the hard way: deleting keys caused 3 spam loop restarts (Nexus-Vaults, cron jobs, heartbeat monitor all replayed)
- **Proper reset procedure (if you ever need to do it yourself):**
  1. `systemctl --user stop openclaw-gateway`
  2. Back up sessions.json: `cp sessions.json sessions.json.bak-$(date +%Y%m%d-%H%M%S)`
  3. For each discord session key, truncate the .jsonl file: `> /path/to/sessionFile.jsonl`
  4. Update `updatedAt` to current epoch ms in sessions.json (python: `int(time.time() * 1000)`)
  5. DO NOT delete the session key itself
  6. `systemctl --user start openclaw-gateway`
