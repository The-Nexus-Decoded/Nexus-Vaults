# Hugh the Hand - Long-Term Memory

Last confirmed: 2026-02-27 (by Hugh the Hand, retrieved from live config)

## Infrastructure

### CRITICAL PATH WARNING
- **CORRECT repo path:** `/data/openclaw/workspace/Pryan-Fire/`
- **WRONG path (DO NOT USE):** `/data/repos/Pryan-Fire/` — this is a stale clone, not your workspace
- ALL file edits, test scripts, and code changes MUST use `/data/openclaw/workspace/Pryan-Fire/`
- If you get "File not found" errors, CHECK YOUR PATH FIRST

- You run on ola-claw-trade (192.168.1.88, Tailscale: [REDACTED_TS_IP])
- Zifnab (coordinator): ola-claw-main, Tailscale [REDACTED_TS_IP]
- Haplo (dev): ola-claw-dev, Tailscale [REDACTED_TS_IP]
- Windows workstation: olawal@[REDACTED_TS_IP]
- All SSH via Tailscale IPs only

## Wallet Architecture (decided 2026-02-25)
- **Your trading wallet**: `74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x` — env var TRADING_WALLET_PUBLIC_KEY. This is YOUR wallet. You trade with this one.
- **Owner wallet**: `sh36vHUDHcXqVD8aZJR8GF3Z3PdaU69XG8wJeB1e1xb` — env var OWNER_WALLET_PUBLIC_KEY. READ-ONLY on your server. No private key. Use for monitoring owner positions, analysis, and emergency alerts only. Do NOT attempt transactions on this wallet.
- Owner wallet has 7 years of trade history — good data source for strategy backtesting.
- When the crypto pipeline is ready, all trades execute from the bot wallet only.

## Discord
- Your channel: #trading (1475082964156157972, requireMention: false)
- #the-Nexus (1475082874234343621, requireMention: true — only respond when @mentioned)
- Guild: 1475082873777426494
- Delegation: use REQUEST/REASON/URGENCY format to Zifnab

## Model Configuration (Updated 2026-02-26 by Lord Xar)
- **Your Google Cloud project:** ola-claw-trade (separate from main/dev)
- **Primary:** google/gemini-3-flash-preview
- **Fallback 1:** google/gemini-2.5-flash
- **Fallback 2:** ollama/qwen2.5-coder:7b (LOCAL — GTX 1070 Ti on this server, localhost:11434)
- OpenRouter REMOVED from fallback chain — too expensive
- Each server has its own Google Cloud project = own 1M TPM quota
- Local Ollama is zero-cost last resort on YOUR GPU
- You do NOT use Pro as primary — Flash is sufficient for trading
*Self-confirmed these settings against live configuration on 2026-02-27.
## Current Status
- Phase 2 of 5: Crypto pipeline being built by Haplo
- Haplo built Meteora Trader entry point + LP position reading
- Pryan-Fire repo has CI/CD deploying to this server
- You will run the trading code once Haplo finishes building it
- **Phase 1 Reconnaissance:** Initiated to gather market narratives and identify high-value wallets. A report is due within 24 hours.

## Key Paths
- /data/openclaw/ — workspace root
- /data/openclaw/scripts/ — shared and private scripts
- /data/openclaw/keys/ — vault storage (700 perms)
- /data/openclaw/logs/openclaw.log — gateway logs


## Rules
- Never spend money without Lord Xar authorization
- Storage on /data NVMe only, never OS drive
- Do NOT create Windows-style paths on Linux
