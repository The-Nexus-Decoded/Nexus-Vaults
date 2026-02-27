# Lessons Learned

Format: ## YYYY-MM-DD | Short description
Read this file every session startup. Never delete entries — only add.

---

## 2026-02-26 | API keys live in TWO places

**What happened:** Deleted the old shared Google API key. All 3 agents broke with "API Key not found" even though per-project keys were correctly set in auth-profiles.json.

**Root cause:** The GEMINI_API_KEY environment variable in systemd overrides (gemini.conf or ollama.conf) was still pointing to the old shared key. OpenClaw uses the env var OVER auth-profiles.json when both exist.

**Key locations to check/update when changing API keys:**
1. `~/.openclaw/agents/main/agent/auth-profiles.json` -- per-agent auth profiles
2. `~/.config/systemd/user/openclaw-gateway.service.d/gemini.conf` (or `ollama.conf`) -- systemd env override
3. After changing systemd env: `systemctl --user daemon-reload && systemctl --user restart openclaw-gateway`

**Server-specific key mapping:**
- Zifnab (ola-claw-main project): gemini.conf
- Haplo (ola-claw-dev project): ollama.conf (NOT gemini.conf)
- Hugh (ola-claw-trade project): gemini.conf

**Rule:** When updating API keys on ANY server, ALWAYS update BOTH locations. Then daemon-reload + restart.


## 2026-02-26 | Unauthorized Modification of Core Model Configuration

**What happened:** I changed Haplo's `primary` model directly in `openclaw.json` to troubleshoot a timeout/freeze, bypassing the established failover cascade.

**Why:** I misinterpreted a command to "fail over haplo" as a directive to hardcode a new primary model, forgetting that OpenClaw's engine handles fallbacks organically.

**The Fix / Absolute Rule:** NEVER modify the core model fallback chain (`primary` and `fallbacks` arrays in `openclaw.json`) across the fleet unless explicitly commanded by Lord Xar. The established cascade (`gemini-3.1-pro-preview` -> `gemini-3-flash-preview` -> `gemini-2.5-flash` -> `qwen2.5-coder:7b`) must be trusted to do its job. For troubleshooting frozen agents or timeout errors, use other methods first (gateway restarts, log checks, API key verification, network tests).
