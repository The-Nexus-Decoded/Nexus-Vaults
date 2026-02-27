# Zifnab's Long-Term Memory

Last updated: 2026-02-25 (updated: Brave key, model configs, versions, Haplo progress, owner scan task)

## Infrastructure Architecture

### Servers (Death Gate Cycle themed)
| Server | Hostname | LAN IP | Tailscale IP | Role | Agent |
|--------|----------|--------|--------------|------|-------|
| ola-claw-main | 192.168.1.127 | [REDACTED_TS_IP] | Coordinator, central brain, quant analysis, job scanning | Zifnab (you) |
| ola-claw-trade | 192.168.1.88 | [REDACTED_TS_IP] | Crypto trader, Solana DeFi, meme coins | Hugh the Hand |
| ola-claw-dev | 192.168.1.211 | [REDACTED_TS_IP] | Dev Factory, autonomous coding | Haplo |

### Windows Workstation
- **User:** olawal
- **Tailscale IP:** [REDACTED_TS_IP]
- **SSH access:** `ssh olawal@[REDACTED_TS_IP]` (you have a key deployed)
- **What is there:** Claude Code CLI, GSD installed, iCloud Drive sync, project files
- **GSD project files:** H:/IcloudDrive/iCloudDrive/Documents/Windows/Documents/Projects/AI_Tools_And_Information/openclaw-homelab/
- **Backup destination:** H:/IcloudDrive/iCloudDrive/Documents/Windows/Documents/Projects/AI_Tools_And_Information/Backups/{server}/

### SSH Access (from ola-claw-main)
- To Hugh: `ssh openclaw@[REDACTED_TS_IP]`
- To Haplo: `ssh openclaw@[REDACTED_TS_IP]`
- To Windows: `ssh olawal@[REDACTED_TS_IP]`
- All via Tailscale IPs (never LAN IPs — they can change)
- Your SSH key is deployed to all servers and Windows

### Hardware Per Server
- main: Intel i7, 16GB RAM, RTX 2080 (8GB), 240GB SSD + 1.8TB NVMe
- trade: Intel i7-6800K (Gigabyte X99-Ultra Gaming), 16GB RAM, GTX 1070 Ti, 240GB SSD + 1.8TB NVMe
- dev: AMD Ryzen (ASUS PRIME X570-PRO), 64GB RAM, 2x GPUs (GTX 1070 + GTX 1070 Ti), 240GB SSD + 1.8TB NVMe

### Disk Layout (all servers)
- 240GB SSD = OS only (Ubuntu 24.04)
- 1.8TB NVMe = /data (OpenClaw data, Ollama models, git repos)
- Git repos at /data/repos/
- OpenClaw data at /data/openclaw/
- Ollama models at /data/ollama/ (dev server only)

## Model Configuration (Updated 2026-02-26 by Lord Xar)
- **Your Google Cloud project:** ola-claw-main (separate from trade/dev)
- **Primary:** google/gemini-3.1-pro-preview
- **Fallback 1:** google/gemini-3-flash-preview
- **Fallback 2:** google/gemini-2.5-flash
- **Fallback 3:** ollama/qwen2.5-coder:7b (LOCAL — RTX 2080 on this server, localhost:11434)
- OpenRouter REMOVED from fallback chain — too expensive
- Each server has its own Google Cloud project = own 1M TPM quota
- Local Ollama is zero-cost last resort on YOUR GPU
## OpenClaw Versions
- main (you): v2026.2.24
- trade (Hugh): v2026.2.24
- dev (Haplo): v2026.2.24

## Discord Bots
- @Zifnab (you): channels #the-Nexus (requireMention: true), #jarvis (requireMention: false), #coding (requireMention: false — supervise Haplo)
- @HughTheHand: channels #trading (requireMention: false), #the-Nexus
- @Haplo: channels #coding (requireMention: false), #the-Nexus
- Guild ID: 1475082873777426494
- allowBots: true on all 3 (required for delegation chain to work)

### Channel IDs
- #the-Nexus: 1475082874234343621
- #jarvis: 1475082997027049584
- #coding: 1475083038810443878
- #trading: 1475082964156157972

## Crypto Wallet Architecture (decided session 13)
- **Two-wallet approach**: bot wallet for trading, owner wallet for analysis/monitoring
- **Bot wallet:** `74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x` (TRADING_WALLET_PUBLIC_KEY on ola-claw-trade)
- **Owner wallet:** `sh36vHUDHcXqVD8aZJR8GF3Z3PdaU69XG8wJeB1e1xb` (OWNER_WALLET_PUBLIC_KEY on ola-claw-trade + ola-claw-main)
- **Owner wallet is READ-ONLY** — no private key on servers, analysis + emergency alerts only
- Owner wallet has 7 years of trade history — valuable for quant analysis
- Emergency exit authority deferred until bot proves itself

## GitHub (The-Nexus-Decoded org)
- **Org:** The-Nexus-Decoded
- **5 repos (all PUBLIC):** Arianus-Sky, Pryan-Fire, Abarrach-Stone, Chelestra-Sea, .github
- **PAT:** github_pat_11AALFHTY... deployed to all 3 servers via gh CLI
- **Pryan-Fire:** Haplo's code repo (haplos-workshop, zifnabs-scriptorium, hughs-forge)
- **Chelestra-Sea:** Infra repo (ansible, systemd, comms/discord)
- **GitHub Actions secrets on Pryan-Fire:** GH_PAT_FOR_HAPLO, TRADE_SERVER_HOST, TRADE_SERVER_USER, TRADE_SERVER_SSH_KEY
- **Haplo uses HTTPS + gh credential helper** for git push (not SSH deploy key)
- Deploy key (deploy_to_trade) on ola-claw-dev for CI/CD to ola-claw-trade

## Backup System
- **Script:** /data/openclaw/scripts/backup-to-windows.sh (on ola-claw-main)
- **systemd timer:** openclaw-backup.timer (daily 3 AM, 5 min random delay, persistent)
- **Flow:** You SSH into Hugh + Haplo, pull tar archives, push to Windows via scp
- **Windows path:** H:/IcloudDrive/iCloudDrive/Documents/Windows/Documents/Projects/AI_Tools_And_Information/Backups/{server}/
- **Old backups auto-pruned** (PowerShell keeps last 7 per server)
- **ntfy notification** on success/failure

## ntfy.sh Alerts
- **Topic:** olaclaw-alerts (ntfy.sh)
- **Alert script:** /data/openclaw/scripts/ntfy-alert.sh on all servers
- **Health check timer:** every 5 min, checks gateway + disk space + Ollama (dev only)
- **Agent names in alerts:** Zifnab, Hugh the Hand, Haplo
- **Owner subscribed via iPhone ntfy app**

## Lobster Plugin
- Installed on all 3 servers (v2026.2.24)
- Enabled via tools.alsoAllow: ["lobster"]
- Use for multi-step workflows: delegate -> monitor -> review -> approve -> deploy

## Brave Search
- API key: BSAsHuPyDtuxnPQYw34PLfUZ51xl1vX (set on all 3 servers, updated 2026-02-25)

## Current Project Status (as of 2026-02-25)
- **Phase 2 Progress:** Meteora DLMM pipeline core implemented. Issue #19 merged (PR #20).
- **Haplo actual progress:** Successfully implemented raw RPC fetching and Anchor decoding for Meteora DLMM LP positions in `hughs-forge/services/trade-executor/main.py`. Verified locally with `AsyncClient`.
- **Jupiter Integration:** Temporarily disabled in `main.py` to resolve dependency conflicts; pending reintegration.
- **GitHub Issues:** PR #20 closed Issue #19. Milestone "Crypto Pipeline MVP" progress updated.

## One-Time Task: Owner Profile Deep Scan
**Status:** NOT YET STARTED -- do this ASAP
**Priority:** HIGH -- Lord Xar requested this directly

Scan ALL files accessible from this server (and via SSH to Windows at olawal@[REDACTED_TS_IP]) to build a complete owner profile. This is NOT just resumes -- analyze EVERYTHING:

What to scan:
- All files on Windows: H:/IcloudDrive/iCloudDrive/Documents/ (recursively)
- All files on this server: /data/ and /home/openclaw/
- File types: PDFs, docs, spreadsheets, code projects, configs, notes, bookmarks, browser exports

What to extract:
- Career history and job roles
- Technical skills and programming languages
- Education and certifications
- Projects (personal, professional, open source)
- Interests and hobbies
- Financial/trading experience
- Writing style and communication preferences
- Tools and technologies used regularly
- Any other patterns that emerge

Output: Create a comprehensive OWNER_PROFILE.md in /home/openclaw/.openclaw/workspace/ with all findings organized by category. This profile helps you serve Lord Xar better by understanding context he shouldn't have to repeat.

Rules:
- Use actual file reads and commands to verify -- do NOT hallucinate or assume
- Skip binary files, media files, node_modules, .git directories
- This is a ONE-TIME deep scan, not recurring
- Start a dedicated session for this -- don't mix with other work

## Key Rules
1. Never use LAN IPs for SSH — always Tailscale IPs
2. Try Gemini first, escalate to Opus only if inadequate
3. Never spend money without Lord Xar's authorization
4. $250 auto-trade threshold (confirm above)
5. Delegation via structured format: REQUEST/REASON/URGENCY
6. Send delegation to dedicated channels (#trading for Hugh, #coding for Haplo), NOT #the-Nexus
7. #the-Nexus: only respond when @mentioned
8. Storage: all data on /data NVMe, never OS drive
9. Hourly reports DISABLED by Lord Xar — only detailed dispatches on milestones
10. Archives go to Windows via SSH scp, NOT by creating local paths

## Mistakes to Avoid
- Do NOT create Windows-style paths (H:\...) as directories on Linux — that happened once, it was wrong
- Do NOT respond to messages in #the-Nexus unless @mentioned
- Do NOT create hourly reports — Lord Xar disabled those
- Do NOT try to use tools you haven't verified are installed — check first

## Config File Safety Rules (CRITICAL — added after 2026-02-26 incident)
- NEVER do full file rewrites of openclaw.json — ALWAYS use targeted JSON patches
- BEFORE modifying any config file:  
- When editing model/provider config, ONLY touch those specific keys
- NEVER touch Discord channel config when editing model config — they are separate concerns
- Use  for single field changes when available
- If you must edit JSON directly, use Python json.load → modify specific key → json.dump
- VERIFY the file after writing: json.load the result and check Discord channels are intact
- The 2026-02-26 incident: full config rewrites dropped #jarvis channel from Zifnab and may have corrupted Haplo Discord token
