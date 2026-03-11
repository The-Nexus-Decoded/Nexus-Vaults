# Fleet Scheduling Reference

All scheduled jobs across the OpenClaw fleet. Updated 2026-02-28.

## Overview

| Job | Server(s) | System | Schedule | Script |
|-----|-----------|--------|----------|--------|
| health-check | ALL 3 | OpenClaw cron | every 5m | `/data/openclaw/scripts/health-check.sh` |
| memory-guard | ALL 3 | OpenClaw cron | every 5m | `/data/repos/Nexus-Vaults/scripts/memory-guard.sh` |
| discord-daily-digest | Zifnab | OpenClaw cron | 8 AM CT | _(agent prompt, no script)_ |
| redact-and-sync | Zifnab | OpenClaw cron | 2 AM CT | `/data/repos/Nexus-Vaults/scripts/redact-and-sync.sh` |
| daily-tithe | Haplo | OpenClaw cron | 10 AM CT | `/data/repos/Pryan-Fire/haplos-workshop/scripts/daily_tithe.sh` |
| fleet_alert_monitor | Zifnab | crontab `*/10` | every 10m | `/data/openclaw/workspace/fleet_alert_monitor.sh` |
| retrieve_windows_logs | Zifnab | crontab `*/5` | every 5m | `/data/openclaw/workspace/retrieve_windows_logs.sh` |

## OpenClaw Cron Management

All OpenClaw crons run as `--session isolated --no-deliver` (except discord-daily-digest which announces to #jarvis).

```bash
openclaw cron list              # show all jobs
openclaw cron run --id <uuid>   # test-run a job
openclaw cron runs --id <uuid>  # show run history
openclaw cron disable <uuid>    # pause a job
openclaw cron enable <uuid>     # resume a job
openclaw cron rm <uuid>         # delete a job
```

### Cron IDs by Server

Run `openclaw cron list` on each server to get current IDs.

---

## Script Source Code

### health-check.sh

Runs on all 3 servers. Checks gateway health, disk space, and Ollama (Haplo only).
Each server has a customized copy with its own `HOSTNAME` variable.

**Path:** `/data/openclaw/scripts/health-check.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPTS_DIR="/data/openclaw/scripts"
HOSTNAME="<server-name>"  # Zifnab, Haplo, or Hugh the Hand
LOCKFILE="/tmp/openclaw-health-alerted"

# Check if gateway is responding
if ! curl -sf http://127.0.0.1:18789/health > /dev/null 2>&1; then
    if [ ! -f "$LOCKFILE" ]; then
        "$SCRIPTS_DIR/ntfy-alert.sh" "Gateway DOWN" \
          "OpenClaw gateway is not responding on $HOSTNAME. Service may need restart." 5
        touch "$LOCKFILE"
    fi
else
    rm -f "$LOCKFILE"
fi

# Check disk space (alert if /data is >90% full)
DATA_USAGE=$(df /data --output=pcent | tail -1 | tr -d ' %')
if [ "$DATA_USAGE" -gt 90 ]; then
    "$SCRIPTS_DIR/ntfy-alert.sh" "Disk Space Critical" "/data is ${DATA_USAGE}% full on $HOSTNAME" 5
fi

# Check if Ollama is expected and running (dev server only)
if [ "$HOSTNAME" = "ola-claw-dev" ]; then
    if ! curl -sf http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then
        if [ ! -f "/tmp/ollama-health-alerted" ]; then
            "$SCRIPTS_DIR/ntfy-alert.sh" "Ollama DOWN" "Ollama is not responding on $HOSTNAME" 4
            touch "/tmp/ollama-health-alerted"
        fi
    else
        rm -f "/tmp/ollama-health-alerted"
    fi
fi
```

---

### memory-guard.sh

Runs on all 3 servers. Protects MEMORY.md from corruption using shadow-copy pattern.
Keeps last 30 backups in `/data/openclaw/workspace/.memory-backups/`.

**Path:** `/data/repos/Nexus-Vaults/scripts/memory-guard.sh`

```bash
#!/usr/bin/env bash

# memory-guard.sh — Backs up MEMORY.md BEFORE it gets overwritten
# Compares checksum, saves old version if changed

WORKSPACE="/data/openclaw/workspace"
MEMORY="$WORKSPACE/MEMORY.md"
BACKUP_DIR="$WORKSPACE/.memory-backups"
CHECKSUM_FILE="$BACKUP_DIR/.last-checksum"
MAX_BACKUPS=30

[ ! -f "$MEMORY" ] && exit 0
mkdir -p "$BACKUP_DIR"

CURRENT=$(md5sum "$MEMORY" | awk '{print $1}')
PREVIOUS=""
[ -f "$CHECKSUM_FILE" ] && PREVIOUS=$(cat "$CHECKSUM_FILE")
[ "$CURRENT" = "$PREVIOUS" ] && exit 0

SHADOW="$BACKUP_DIR/.shadow-MEMORY.md"

if [ -f "$SHADOW" ]; then
    TS=$(date +%Y%m%d-%H%M%S)
    cp "$SHADOW" "$BACKUP_DIR/MEMORY-${TS}.md"
fi

cp "$MEMORY" "$SHADOW"
echo "$CURRENT" > "$CHECKSUM_FILE"

cd "$BACKUP_DIR"
ls -t MEMORY-*.md 2>/dev/null | tail -n +$((MAX_BACKUPS + 1)) | xargs rm -f 2>/dev/null
exit 0
```

---

### redact-and-sync.sh (Zifnab only)

Daily workspace backup. Rsyncs all 3 agents' workspaces, redacts secrets, commits to Nexus-Vaults repo.

**Path:** `/data/repos/Nexus-Vaults/scripts/redact-and-sync.sh`

```bash
#!/usr/bin/env bash
# redact-and-sync.sh — Fleet workspace backup with redaction
# Syncs all 3 agents' workspaces to Nexus-Vaults repo
# Usage: ./redact-and-sync.sh [--dry-run]

set -e

REPO_DIR="/data/repos/Nexus-Vaults"
KEYS_DIR="/data/openclaw/keys"

EXCLUDE=(
  --exclude 'node_modules/' --exclude 'venv/' --exclude '.venv/'
  --exclude '.git/' --exclude '__pycache__/' --exclude '*.db'
  --exclude '*.sqlite' --exclude '*.pyc' --exclude '*.jsonl'
  --exclude 'owner_intelligence/' --exclude 'nexus-vaults-restore/'
  --exclude 'OWNER_PROFILE_RAW.md' --exclude '*.bak*'
  --exclude '*.pre-sync*' --exclude 'staging_windows_docs/'
  --exclude 'document_index.db' --exclude 'testvenv/'
  --exclude 'site-packages/'
)

SERVERS=(
  "ola-claw-main:local:/data/openclaw/workspace"
  "ola-claw-trade:ssh:<trade-tailscale-ip>:/data/openclaw/workspace"
  "ola-claw-dev:ssh:<dev-tailscale-ip>:/data/openclaw/workspace"
)

# For each server: rsync workspace to staging, redact secrets, copy to repo
# Redaction covers: GitHub PATs, API keys, Google keys, Bearer [REDACTED][REDACTED][REDACTED][REDACTED][REDACTED][REDACTED],
# Tailscale IPs, Discord tokens, and any keys in $KEYS_DIR
# Pre-commit hook scans diff for un-redacted secrets and aborts if found
# Then commits and pushes to origin
```

---

### daily_tithe.sh (Haplo only)

Solana devnet airdrop for Pryan-Fire development.

**Path:** `/data/repos/Pryan-Fire/haplos-workshop/scripts/daily_tithe.sh`

```bash
#!/bin/bash
# The Daily Tithe - Automated SOL Harvest

echo "[$(date)] Striking the celestial font..."
solana airdrop 2 <wallet-address> --url devnet
echo "[$(date)] Tithe collected."
```

---

### fleet_alert_monitor.sh (Zifnab crontab only)

Posts fleet status to #jarvis every 10 minutes. Uses `fleet_parse.py` to parse rate guard health data.

**Path:** `/data/openclaw/workspace/fleet_alert_monitor.sh`
**Parser:** `/data/openclaw/workspace/fleet_parse.py`

```bash
#!/bin/bash
# Fleet Status Monitor — services + rate guard summary per server
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus

JARVIS_CHANNEL="<discord-channel-id>"
DISCORD_BOT_TOKEN=$(python3 -c "import json; ..." 2>/dev/null)
PARSER="/data/openclaw/workspace/fleet_parse.py"

SERVERS="zifnab:local haplo:ssh:<dev-ip> hugh:ssh:<trade-ip>"

# For each server (local curl or SSH):
#   - Check systemctl --user is-active for gateway + rate-guard
#   - Curl rate guard /health endpoint
#   - Parse with fleet_parse.py (filters to active API key, tags ACTIVE/EXHAUSTED)
#   - Build Discord message with code blocks
# Posts formatted fleet status to #jarvis via Discord bot API
```

**fleet_parse.py** — Parses rate guard `/health` JSON:
- Filters models to active API key only (hides overflow key clutter)
- Shows per-model: RPD used/budget, TPM-day cumulative, RPM/TPM sliding window with budgets, 429 count
- Tags active model `[ACTIVE !!]`, exhausted models `[EXHAUSTED]`
- Summary line: daily RPD %, current RPM/TPM totals, peak RPM/TPM %

---

## Migration History

**2026-02-28:** Migrated from crontab/systemd to OpenClaw crons:
- `openclaw-health-check` systemd timer -> OpenClaw cron (all 3 servers)
- `memory-guard.sh` crontab -> OpenClaw cron (all 3 servers)
- `redact-and-sync.sh` crontab -> OpenClaw cron (Zifnab)
- `daily_tithe.sh` crontab -> OpenClaw cron (Haplo)

**Remaining on crontab (Zifnab only):**
- `fleet_alert_monitor.sh` — stays on crontab (just fixed, working)
- `retrieve_windows_logs.sh` — stays on crontab (Zifnab's code)

---

## Rate Guard Proxy Fix (2026-02-28) — Chelestra-Sea#26

### Problem
Rate guard proxy at localhost:8787 was completely bypassed on all 3 servers. Two root causes:
1. **Vendor files** had hardcoded `https://generativelanguage.googleapis.com` URLs (21 files across @mariozechner/pi-ai, @google/genai, OpenClaw dist)
2. **gemini.conf corruption** — Zifnab's had `-e` prefix from bad `echo -e`, Haplo had none. GEMINI_API_KEY env var never reached gateway process.

### Fix
1. `sudo bash /data/openclaw/rate-guard-v2/reapply-rate-guard-patches.sh` — patches 21 vendor files (idempotent)
2. Fixed gemini.conf on all servers using `printf` (never `echo -e`)
3. `rm -rf ~/.cache/node/compile_cache && systemctl --user daemon-reload && systemctl --user restart openclaw-gateway`

### Post-update rule
Vendor patches are overwritten by OpenClaw updates. After ANY update: run reapply script + clear cache + restart.

### Verification
Rate guard logs show requests flowing through proxy on all 3 servers. Overflow keys activate on 429s.
