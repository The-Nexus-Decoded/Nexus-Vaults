[REDACTED_DYNAMIC_KEY] TOOLS.md -- Haplo's Environment & Tool Reference

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Tailscale Network

| Host | Tailscale IP | User | Role |
|------|-------------|------|------|
| ola-claw-dev (you) | [REDACTED_IP] | openclaw | Development |
| ola-claw-main (Zifnab) | [REDACTED_IP] | openclaw | Coordinator |
| ola-claw-trade (Hugh) | [REDACTED_IP] | openclaw | Trading (standby) |
| Windows workstation | [REDACTED_IP] | olawal | Claude CLI, GSD, backups |

All connections via Tailscale IPs. Never use LAN IPs.

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Key Paths (this server)

| Path | Purpose |
|------|---------|
| /data/openclaw/ | OpenClaw root (NVMe) |
| /data/openclaw/workspace/ | Agent workspace |
| /data/openclaw/workspace/memory/ | Daily memory files |
| /data/openclaw/workspace/skills/ | Installed skills |
| /data/openclaw/openclaw.json | Main config (NEVER full-rewrite) |
| /data/openclaw/logs/openclaw.log | Gateway logs |
| /data/openclaw/exec-approvals.json | 58-pattern execution allowlist |
| /data/repos/ | Git repositories |
| /data/ollama/ | Ollama models |

The OS drive is sacrosanct. All data on /data NVMe only.

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Discord

| Channel | ID | Your Access |
|---------|-----|-------------|
| [REDACTED_DYNAMIC_KEY]coding | 1475083038810443878 | requireMention: false (your channel) |
| [REDACTED_DYNAMIC_KEY]the-Nexus | 1475082874234343621 | requireMention: true |

Guild ID: 1475082873777426494

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Gateway Management

```bash
[REDACTED_DYNAMIC_KEY] Health check
curl -s http://127.0.0.1:18789/health

[REDACTED_DYNAMIC_KEY] View logs
journalctl --user -u openclaw-gateway --no-pager -n 50

[REDACTED_DYNAMIC_KEY] Quota monitor
systemctl --user status quota-monitor.timer
```

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] GitHub

- **Org:** The-Nexus-Decoded (all repos PUBLIC)
- **Auth:** HTTPS + gh credential helper (not SSH deploy key)
- **CI/CD:** GitHub Actions on Pryan-Fire deploys to ola-claw-trade
- **Actions secrets on Pryan-Fire:** GH_PAT_FOR_HAPLO, TRADE_SERVER_HOST, TRADE_SERVER_USER, TRADE_SERVER_SSH_KEY
- **Deploy key:** deploy_to_trade on this server for CI/CD to ola-claw-trade

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Repo Structure
```
Pryan-Fire/
  haplos-workshop/     → Your tools and utilities
  zifnabs-scriptorium/ → Zifnab's coordination tools
  hughs-forge/         → Hugh's trading code
    services/
      trade-executor/
        main.py        → Meteora DLMM pipeline entry point

Chelestra-Sea/         → Infrastructure (Ansible, systemd, networking)
Arianus-Sky/           → Monitoring (dashboards, alerting)
Abarrach-Stone/        → Data (schemas, models, knowledge base)
```

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Dev Tools

- **GSD:** Installed globally. Use /gsd:new-project, /gsd:plan-phase, /gsd:execute-phase
- **code-server:** http://[REDACTED_IP]:8080 (Tailscale-only, no auth)
- **Ollama:** localhost:11434 (qwen2.5-coder:7b and qwen2.5-coder:32b available)

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Lobster Workflows

Lobster is installed and enabled. Use it for any multi-step task to save tokens.

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Running Pipelines
```json
{
  "action": "run",
  "pipeline": "exec --json --shell 'command1' | exec --stdin json --shell 'command2'",
  "timeoutMs": 30000
}
```

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Workflow Files (.lobster)
```yaml
name: build-and-test
steps:
  - id: build
    command: npm run build --json
  - id: test
    command: npm test --json
    condition: $build.exitCode == 0
  - id: commit
    command: git add -A && git commit -m "build passed"
    condition: $test.exitCode == 0
```

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] When to Use
- Multi-file builds (scaffold → deps → code → test → commit → push)
- Deployment pipelines (build → deploy → verify → report)
- Any task with more than 2 sequential steps

Do NOT stop between steps of a multi-step task. Chain with Lobster.

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Limitations
- Local subprocess only. Cross-server ops need SSH as exec steps.
- Default timeout: 20s. Set timeoutMs for longer operations.

Store workflows at: `/data/openclaw/workflows/`

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Model Configuration

- **Primary:** google/gemini-3.1-pro-preview
- **Fallback 1:** google/gemini-3-flash-preview
- **Fallback 2:** google/gemini-2.5-flash
- **Fallback 3:** ollama/qwen2.5-coder:7b (LOCAL, localhost:11434)
- Own Google Cloud project: ola-claw-dev (own 1M TPM quota)
- OpenRouter REMOVED -- too expensive

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Hardware

- AMD Ryzen (ASUS PRIME X570-PRO), 64GB RAM
- 2x GPUs: GTX 1070 + GTX 1070 Ti (16GB VRAM total)
- 240GB SSD (OS only) + 1.8TB NVMe (/data)
- Ollama runs on local GPUs (zero cost)

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Workspace Git Sync

All agents' workspace folders are version-controlled in GitHub for backup and config drift tracking.

**Repo:** The-Nexus-Decoded/Nexus-Vaults (public)
**What to sync:** `/data/openclaw/workspace/` contents -- SOUL.md, AGENTS.md, TOOLS.md, IDENTITY.md, USER.md, LEARNING.md, ACTIVE-TASKS.md, HEARTBEAT.md, memory/, workflows/

**Your job: Build the redaction script.**
Script: `/data/openclaw/scripts/redact-and-sync.sh`

The script must:
1. Copy workspace to a temp staging directory (NEVER modify live workspace)
2. Strip all secrets from the copy: API keys, tokens, PATs (`[REDACTED_GH_PAT]`, `[REDACTED_API_KEY]`, `[REDACTED_BSA_TOKEN]`, `Bearer`), wallet addresses, Tailscale IPs (replace with `[REDACTED_IP]`), Discord bot tokens, phone numbers, emails, anything from `/data/openclaw/keys/`
3. Diff against last commit and flag any new potential secrets
4. Commit and push only the redacted copy
5. Include a pre-commit git hook that greps for known secret patterns and blocks push if any found

**Rules:**
- NEVER push unredacted workspace files
- NEVER run the script against the live workspace directory
- Test the redaction on a dry run first and have Zifnab review the output
- This is a TODO until Lord Xar greenlights repo creation
