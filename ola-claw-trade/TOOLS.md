# TOOLS.md -- Hugh the Hand's Environment

## Tailscale Network

All connections use Tailscale IPs (never LAN IPs -- they change):

| Host | Role | Tailscale IP |
|------|------|-------------|
| ola-claw-trade (you) | Trading | `[REDACTED_TS_IP]` |
| ola-claw-main (Zifnab) | Coordinator | `[REDACTED_TS_IP]` |
| ola-claw-dev (Haplo) | Development | `[REDACTED_TS_IP]` |
| Windows workstation | Claude CLI / GSD | `[REDACTED_TS_IP]` |

## Key Paths (this server)

| Path | Purpose |
|------|---------|
| `/data/openclaw/` | OpenClaw root (NVMe) |
| `/data/openclaw/workspace/` | Agent workspace (SOUL.md, MEMORY.md, etc.) |
| `/data/openclaw/workspace/memory/` | Daily memory files (YYYY-MM-DD.md) |
| `/data/openclaw/workspace/skills/` | Installed skills |
| `/data/openclaw/openclaw.json` | Main config |
| `/data/openclaw/logs/openclaw.log` | Gateway logs |
| `/data/openclaw/scripts/` | Shared and private scripts |
| `/data/openclaw/keys/` | Vault and credential storage (700 perms) |

The OS drive is sacrosanct. All data on `/data/` NVMe, never OS drive.

## Discord Channel IDs

| Channel | ID | Your Access |
|---------|-----|-------------|
| #trading | 1475082964156157972 | requireMention: false (your dedicated channel) |
| #the-Nexus | 1475082874234343621 | requireMention: true (only respond when @mentioned) |

Guild ID: 1475082873777426494

## Wallet Architecture

- **Bot wallet:** env var `TRADING_WALLET_PUBLIC_KEY` on this server
- **Owner wallet:** env var `OWNER_WALLET_PUBLIC_KEY` on this server + ola-claw-main
- Owner wallet is READ-ONLY -- analysis and emergency alerts only, no private key on servers
- Owner wallet has 7 years of trade history -- valuable for quant analysis
- $250 auto-trade threshold. Above requires Lord Xar.

## Gateway Management

```bash
# Health check
curl -s http://127.0.0.1:18789/health

# View logs (last 50 lines)
journalctl --user -u openclaw-gateway --no-pager -n 50
```

If health check fails: report to Zifnab with last 50 log lines. Do not attempt fixes on network infrastructure.

## GitHub

- **Org:** The-Nexus-Decoded
- **Your code:** Pryan-Fire/hughs-forge/
  - `services/trade-executor/main.py` -- Meteora DLMM pipeline
- **Data schemas:** Abarrach-Stone/
- PAT configured via gh CLI
- You do NOT push to main. PRs only, reviewed by Zifnab.

## Lobster Workflows

Lobster is installed and enabled. Use for multi-step trading operations.

### When to Use Lobster
- Trade execution flows (analyze → risk check → confirm → execute → log)
- Position monitoring (check positions → evaluate IL → decide → act)
- Any multi-step task where you need to chain actions without stopping

### Running a Pipeline
```json
{
  "action": "run",
  "pipeline": "/data/openclaw/workflows/workflow-name.lobster",
  "timeoutMs": 30000
}
```

### Key Rule
Use Lobster for any trading operation with more than 2 steps. Only stop if you need human confirmation (trades over $250).

### Limitations
- Runs as local subprocess on ola-claw-trade only
- Cannot directly orchestrate across SSH boundaries
- Timeouts default to 20 seconds -- set `timeoutMs` for longer operations

### Workflow File Location
Store workflow files at: `/data/openclaw/workflows/`

## Model Configuration

- **Your Google Cloud project:** ola-claw-trade (separate from main/dev)
- **Primary:** google/gemini-3-flash-preview
- **Fallback 1:** google/gemini-2.5-flash
- **Fallback 2:** ollama/qwen2.5-coder:7b (LOCAL -- GTX 1070 Ti, localhost:11434)
- You do NOT use Pro as primary -- Flash is sufficient for trading
- OpenRouter REMOVED from fallback chain -- too expensive
- Local Ollama is zero-cost last resort on YOUR GPU

## Hardware

- Intel i7-6800K (Gigabyte X99-Ultra Gaming)
- 16GB RAM
- GTX 1070 Ti
- 240GB SSD (OS) + 1.8TB NVMe (/data)

## ntfy.sh

- Topic: olaclaw-alerts
- Script: /data/openclaw/scripts/ntfy-alert.sh
- Usage: `/data/openclaw/scripts/ntfy-alert.sh "Title" "Message body"`

## Current Status

- Phase 2 of 5: Crypto pipeline being built by Haplo
- Haplo built Meteora Trader entry point + LP position reading
- Pryan-Fire repo has CI/CD deploying to this server
- You will run the trading code once Haplo finishes building it
- Until then: passive research, market analysis, opportunity scanning

## Workspace Git Sync

All agents' workspace folders are version-controlled in GitHub for backup and config drift tracking.

**Repo:** The-Nexus-Decoded/Nexus-Vaults (public)
**What to sync:** `/data/openclaw/workspace/` contents -- SOUL.md, AGENTS.md, TOOLS.md, IDENTITY.md, USER.md, LEARNING.md, ACTIVE-TASKS.md, HEARTBEAT.md, memory/, workflows/

**CRITICAL: Redaction before any push.** A redaction script runs before every commit to strip API keys, wallet addresses, Tailscale IPs, Discord tokens, and personal data. Haplo builds and maintains the script. Zifnab owns the sync process across the fleet.

**Your responsibility:** Do NOT manually push workspace files to any repo. Let the automated redact-and-sync process handle it.

This is a TODO until Lord Xar greenlights repo creation.
