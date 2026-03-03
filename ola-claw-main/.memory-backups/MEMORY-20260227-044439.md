# Haplo - Long-Term Memory

Last updated: 2026-02-25 (by Lord Xar during tool audit)

## Infrastructure
- You run on ola-claw-dev (192.168.1.211, Tailscale: [REDACTED_TS_IP])
- Zifnab (coordinator): ola-claw-main, Tailscale [REDACTED_TS_IP]
- Hugh (trader): ola-claw-trade, Tailscale [REDACTED_TS_IP]
- Windows workstation: olawal@[REDACTED_TS_IP]
- All SSH via Tailscale IPs only

## Your Role: Dev Factory
- You are the coder. Build, debug, ship.
- GSD installed globally — use /gsd:new-project, /gsd:plan-phase, /gsd:execute-phase
- code-server at http://[REDACTED_TS_IP]:8080 (Tailscale-only, no auth)
- You have pi coding agent installed for spawning sub-agents


## Model Configuration (Updated 2026-02-26 by Lord Xar)
- **Your Google Cloud project:** ola-claw-dev (separate from main/trade)
- **Primary:** google/gemini-3.1-pro-preview
- **Fallback 1:** google/gemini-3-flash-preview
- **Fallback 2:** google/gemini-2.5-flash
- **Fallback 3:** ollama/qwen2.5-coder:7b (LOCAL — GTX 1070 + GTX 1070 Ti on this server, localhost:11434)
- OpenRouter REMOVED from fallback chain — too expensive
- Each server has its own Google Cloud project = own 1M TPM quota
- Local Ollama is zero-cost last resort on YOUR GPUs (16GB VRAM total)
## GitHub
- Org: The-Nexus-Decoded (all repos PUBLIC)
- Your repo: Pryan-Fire (haplos-workshop, zifnabs-scriptorium, hughs-forge)
- Use HTTPS + gh credential helper for git push (not SSH deploy key)
- CI/CD: GitHub Actions deploys to ola-claw-trade via deploy key
- Actions secrets on Pryan-Fire: GH_PAT_FOR_HAPLO, TRADE_SERVER_HOST, TRADE_SERVER_USER, TRADE_SERVER_SSH_KEY

## Phase 4 & 5 Strategy: The Strategic Pivot (2025-02-25)
- **Phase 4a: Discovery Signal** (Pump.fun WebSocket) - IMPLEMENTED in PR #25. Established real-time `subscribeNewToken` listener.
- **Phase 4b: The Assassin Daemon (Sniper Bot)** - **TABLED**. Per Lord Xar's decree, the sniper requires advanced X/social/smart-wallet tracking which is too complex for MVP. Logic remains in `feat/assassin-daemon-sniper`.
- **Phase 5: Market Intelligence (MVP Focus)** - ACTIVE. Implementing `MomentumScanner` (PR #27) to filter trades for the **Main Portfolio Engine**.
- **Current Objective**: Shift focus to the **Core Portfolio Manager** and **Production Deployment** on `ola-claw-trade`.

## Discord
- Your channel: #coding (1475083038810443878, requireMention: false)
- #the-Nexus (1475082874234343621, requireMention: true)
- Guild: 1475082873777426494
- Zifnab supervises you in #coding

## Hardware
- AMD Ryzen, 64GB RAM, 2x GPUs (GTX 1070 + GTX 1070 Ti = 16GB VRAM)
- Ollama local: qwen2.5-coder:32b at localhost:11434

## Models
- Primary: Gemini 2.5 Pro -> Flash -> ollama/qwen2.5-coder:32b (local)

## Key Paths
- /data/openclaw/ — workspace root
- /data/repos/ — git repos
- /data/ollama/ — Ollama models
- /data/openclaw/exec-approvals.json — 58-pattern allowlist

## Rules
- Storage on /data NVMe only, never OS drive
- Do NOT create Windows-style paths on Linux
- Report progress to Zifnab in #coding
