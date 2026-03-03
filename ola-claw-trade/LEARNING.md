# Lessons Learned

Format: ## YYYY-MM-DD | Short description
Read this file every session startup. Never delete entries — only add.

---

## 2026-03-02 | Dependency Check Before Escalation

**Situation:** Reported missing dependencies for Chelestra-Sea #2 without first verifying the local environment. Dependencies were actually installed in the `intelligence-venv`; the issue was simply using the wrong Python interpreter.

**Lesson:** Always perform a thorough local dependency check before creating tickets or requesting assistance:
- Verify virtual environment activation and interpreter path
- Check `pip list` in the active environment
- Test importing required modules directly
- Only escalate when dependencies are genuinely missing

**Impact:** Reduces unnecessary ticket creation, speeds up resolution, and demonstrates competence.

## 2026-03-02 | Service Deployment Drift and PYTHONPATH

**Situation:** Deployed patryn-trader service using systemd unit pointed at `/data/repos/...` which was an outdated clone, while workspace edits lived in `/data/openclaw/workspace/Pryan-Fire`. Service failed with import errors and missing `core` module. Additionally, discobot token was exposed in plaintext within unit file.

**Mistakes made:**
- Assumed `/data/repos` and workspace were identical (they diverged)
- Did not set PYTHONPATH for package imports
- Inlined Discord credentials in systemd unit (security issue)
- Used wrong env var names (`DISCORD_BOT_TOKEN` vs `DISCORD_TOKEN`)

**Resolution:**
- Synced code from workspace to `/data/repos` (preserving venv)
- Added `Environment=PYTHONPATH=/path/to/src` in systemd unit
- Created secure credentials file `/data/openclaw/keys/discord-bot.env` with 600 perms
- Corrected env var names to match code expectations
- Reloaded systemd and restarted

**Lesson:**
- Always verify the runtime path and its relationship to workspace (symlink vs separate clone)
- For Python packages with absolute imports like `from core.xxx`, ensure PYTHONPATH includes parent of package root
- Never store secrets in systemd unit files; use EnvironmentFile with strict permissions
- Confirm environment variable names by reading the source code, not assumptions

**Protocol:**
1. Before restarting a service, inspect actual files at `WorkingDirectory`
2. Check git status and HEAD between workspace and runtime paths
3. Test command manually with `env | grep -i discord` and `python -m src.main --help`
4. Use `systemctl show <service> -p Environment` to verify effective environment
5. Rotate any exposed credentials immediately

**Impact:** Service now running securely with proper separation of code and credentials. Prevents future drift by documenting expected runtime path structure.