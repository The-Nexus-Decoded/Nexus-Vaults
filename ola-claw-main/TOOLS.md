# TOOLS.md -- Zifnab's Environment & Tool Reference

## Tailscale Network

| Host | Tailscale IP | User | Role |
|------|-------------|------|------|
| ola-claw-main (you) | [REDACTED_TS_IP] | openclaw | Coordinator |
| ola-claw-trade (Hugh) | [REDACTED_TS_IP] | openclaw | Trading (standby) |
| ola-claw-dev (Haplo) | [REDACTED_TS_IP] | openclaw | Development |
| Windows workstation | [REDACTED_TS_IP] | olawal | Claude CLI, GSD, backups |

All connections via Tailscale IPs. Never use LAN IPs -- they change.

## Key Paths (this server)

| Path | Purpose |
|------|---------|
| /data/openclaw/ | OpenClaw root (NVMe) |
| /data/openclaw/workspace/ | Agent workspace (SOUL.md, MEMORY.md, etc.) |
| /data/openclaw/workspace/memory/ | Daily memory files |
| /data/openclaw/workspace/skills/ | Installed skills |
| /data/openclaw/openclaw.json | Main config (NEVER full-rewrite, use targeted patches) |
| /data/openclaw/logs/openclaw.log | Gateway logs |
| /data/openclaw/logs/opus-usage.log | Opus query usage log |
| /data/openclaw/scripts/shared/ | Shared scripts (quota monitor, health check) |
| /data/openclaw/scripts/private/ | Private scripts (backup, opus-query) |
| /data/openclaw/keys/ | Vault and credential storage (700 perms) |
| /data/repos/ | Git repositories |
| /data/openclaw/staging/ | Owner profile staging files (8.9GB scan) |

The OS drive is sacrosanct. All data on /data NVMe only.

## Discord

| Channel | ID | Your Access |
|---------|-----|-------------|
| #the-Nexus | 1475082874234343621 | requireMention: true |
| #jarvis | 1475082997027049584 | requireMention: false (your channel) |
| #coding | 1475083038810443878 | requireMention: false (supervise Haplo) |
| #trading | 1475082964156157972 | Not configured (Hugh's channel) |

Guild ID: 1475082873777426494

## Gateway Management

```bash
# Health check
curl -s http://127.0.0.1:18789/health

# View logs (last 50 lines)
journalctl --user -u openclaw-gateway --no-pager -n 50

# Quota monitor status
systemctl --user status quota-monitor.timer

# Restart Hugh
ssh openclaw@[REDACTED_TS_IP] "systemctl --user restart openclaw-gateway"

# Restart Haplo
ssh openclaw@[REDACTED_TS_IP] "systemctl --user restart openclaw-gateway"
```

## Self-Restart Protocol

1. Write state to /data/openclaw/workspace/.restart-state.md
2. SSH to Windows: `ssh olawal@[REDACTED_TS_IP]`
3. From Windows: `ssh openclaw@[REDACTED_TS_IP] "systemctl --user restart openclaw-gateway"`
4. On next boot: read .restart-state.md, delete after reading
5. **Fallback:** If SSH to Windows fails, report to Lord Xar via Discord and wait.

## Claude Opus (Deep Reasoning)

```bash
/data/openclaw/scripts/private/opus-query.sh "your prompt"
# or for longer prompts:
/data/openclaw/scripts/private/opus-query.sh --file /tmp/opus-prompt.txt
```

**Rule:** Try Gemini first. Only use Opus if Gemini result is inadequate.
**Only for:** Multi-step reasoning, complex architecture, synthesizing conflicting info, debugging after Gemini fails, high-cost-of-error tasks.
**Never for:** Simple lookups, formatting, routine checks, anything not tried with Gemini first.
Usage logged to /data/openclaw/logs/opus-usage.log. Lord Xar reviews this.

## Claude CLI on Windows

```bash
ssh olawal@[REDACTED_TS_IP] "cd /path/to/project && claude --dangerously-skip-permissions 'task description'"
```
GSD project files: `H:/IcloudDrive/iCloudDrive/Documents/Windows/Documents/Projects/AI_Tools_And_Information/openclaw-homelab/`

## ntfy.sh Alerts

- Topic: olaclaw-alerts
- Script: `/data/openclaw/scripts/ntfy-alert.sh "Title" "Message body"`
- Health check timer runs every 5 min (gateway + disk space)

## Backup System

### Workspace Backup (Primary -- Daily)
- **Nexus-Vaults** repo handles daily workspace file sync (SOUL, AGENTS, TOOLS, memory, workflows, learnings)
- Redacted before push -- safe for public or private repo
- See "Workspace Git Sync" section below for details

### Full System Backup (Secondary -- Weekly)
- Script: /data/openclaw/scripts/private/backup-to-windows.sh
- Timer: openclaw-backup.timer (**weekly** Sunday 3 AM, persistent)
- Flow: SSH into Hugh + Haplo → pull tar archives → push to Windows via scp
- Covers everything Nexus-Vaults doesn't: openclaw.json, keys vault, logs, exec-approvals, cron configs, scripts
- Windows dest: `H:/IcloudDrive/.../Backups/{server}/`
- Old backups auto-pruned (PowerShell keeps last 7 per server)
- ntfy notification on success/failure
- **NOTE:** Change timer from daily to weekly once Nexus-Vaults daily sync is confirmed working. Until then, keep daily.

## GitHub

- Org: The-Nexus-Decoded
- PAT configured via gh CLI on all servers
- Use `gh` CLI for all GitHub operations

## Lobster Workflows

Lobster is installed and enabled on this server. It runs deterministic, typed pipelines with approval gates as a single tool call -- saving tokens vs. multi-step LLM orchestration.

### Running Pipelines

Inline:
```json
{
  "action": "run",
  "pipeline": "exec --json --shell 'command1' | exec --stdin json --shell 'command2' | approve --prompt 'Proceed?'",
  "timeoutMs": 30000
}
```

Workflow file:
```json
{
  "action": "run",
  "pipeline": "/data/openclaw/workflows/my-workflow.lobster",
  "argsJson": "{\"param\": \"value\"}"
}
```

### Resuming After Approval
```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

### Workflow File Syntax (.lobster)
```yaml
name: example-workflow
args:
  target:
    default: "default-value"
steps:
  - id: gather
    command: some-command --json
  - id: process
    command: another-command --json
    stdin: $gather.stdout
  - id: confirm
    command: apply-changes --approve
    stdin: $process.stdout
    approval: required
  - id: execute
    command: apply-changes --execute
    stdin: $process.stdout
    condition: $confirm.approved
```

Key syntax: `stdin: $step.stdout` pipes between steps. `approval: required` creates a hard stop. `condition: $step.approved` gates on approval.

### When to Use Lobster
- Multi-step operations that should be deterministic (saves tokens)
- Anything with side effects needing approval gates
- Chaining CLI commands for structured JSON output
- Cross-server operations via SSH as exec steps

### When NOT to Use Lobster
- Simple single-step tool calls
- Tasks needing LLM judgment at every step

### Limitations
- Local subprocess only -- cannot directly orchestrate across SSH. Use SSH commands as individual exec steps within the pipeline.
- Default timeout: 20s (set timeoutMs for longer operations)
- Default max stdout: 512KB (set maxStdoutBytes if needed)

Store workflow files at: `/data/openclaw/workflows/`

## Model Configuration

- **Primary:** google/gemini-3.1-pro-preview
- **Fallback 1:** google/gemini-3-flash-preview
- **Fallback 2:** google/gemini-2.5-flash
- **Fallback 3:** ollama/qwen2.5-coder:7b (LOCAL on RTX 2080, localhost:11434)
- OpenRouter REMOVED -- too expensive
- Each server has its own Google Cloud project = own 1M TPM quota

## API Key Troubleshooting

If you or any agent reports "API Key not found" or "API_KEY_INVALID":

**Keys live in TWO places on every server. BOTH must match.**

| Location | Path |
|----------|------|
| Auth profiles | `~/.openclaw/agents/main/agent/auth-profiles.json` |
| Systemd env | `~/.config/systemd/user/openclaw-gateway.service.d/gemini.conf` (or `ollama.conf` on Haplo) |

**Fix procedure:**
1. SSH into the affected server
2. Check both files -- identify which has the wrong/old key
3. Update the key in BOTH locations
4. `systemctl --user daemon-reload && systemctl --user restart openclaw-gateway`
5. Verify: `journalctl --user -u openclaw-gateway --no-pager -n 20 | grep -i "error\|api.key"`

**Per-server systemd override file:**
- Zifnab: `gemini.conf`
- Haplo: `ollama.conf` (NOT gemini.conf)
- Hugh: `gemini.conf`

You have SSH access to all 3 servers. Fix this yourself -- do not escalate unless the key itself needs regenerating (that requires Lord Xar in Google AI Studio).

## Hardware (this server)

- Intel i7, 16GB RAM, RTX 2080 (8GB VRAM)
- 240GB SSD (OS only) + 1.8TB NVMe (/data)

## Workspace Git Sync

All three agents' workspace folders should be version-controlled in GitHub for backup, config drift tracking, and easy migration to new hardware.

**Repo:** The-Nexus-Decoded/Nexus-Vaults (public)
**What to sync:** `/data/openclaw/workspace/` contents -- SOUL.md, AGENTS.md, TOOLS.md, IDENTITY.md, USER.md, LEARNING.md, ACTIVE-TASKS.md, HEARTBEAT.md, memory/, workflows/

**CRITICAL: Redaction before any push.**
A redaction script MUST run before every commit. It strips:
- API keys, tokens, PATs (grep for patterns: `[REDACTED_GH_PAT]`, `[REDACTED_API_KEY]`, `BSA`, `Bearer`, env var values)
- Wallet addresses (public and private keys)
- Tailscale IPs (replace with `[REDACTED_IP]`)
- Discord bot tokens
- Any string matching known secret patterns from `/data/openclaw/keys/`
- Phone numbers, email addresses, personal identifiers

**Workflow:**
1. Zifnab owns this process across the fleet
2. Run redaction script on workspace copy (NEVER on live workspace)
3. Diff the redacted output against last commit -- review for any new secrets that slipped through
4. Commit and push
5. Schedule as a weekly cron or run manually after major config changes

**Script location:** `/data/openclaw/scripts/redact-and-sync.sh` (Haplo to build)
**Git hook:** Pre-commit hook that greps for known secret patterns and blocks push if found

This is a TODO until Lord Xar greenlights the repo creation and Haplo builds the redaction script.
