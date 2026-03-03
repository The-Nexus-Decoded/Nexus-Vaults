# Active Tasks

Ongoing crons, recurring jobs, multi-session projects.
Each task gets its own section. Archive completed tasks, don't delete.

---

## Chelestra-Sea #2 - Profile Distillation (2026-03-02) ✅ COMPLETED

**Objective:** Build an intelligence database from the 24,088-file Windows archive using SQLite + ChromaDB.

**Final Results:**
- **Files processed:** 22,630
- **Errors:** 44 (corrupted/unreadable, expected)
- **Database:** SQLite + ChromaDB fully built and indexed
- **Location:** `/data/intelligence/`

**Notes:** Archive extraction completed 2026-03-02 01:15:17 CST. Ready for query interface development.

**Owner:** Hugh the Hand

**→ Next:** Chelestra-Sea #3 (Intelligence Query API) — blocked on Jupiter functionality

---

## Pryan-Fire #141: Jupiter Service Deployment (2026-03-02) ✅ COMPLETED

**Objective:** Deploy the Patryn Trade Orchestrator with Jupiter integration capability.

**Resolution:** Adopted modern event-driven architecture (`src.main`) which bypasses the RiskManager/Discord dependency. Service is running and initialized.

**Status:** SERVICE_RUNNING

**Completed:**
- [x] Fixed systemd service (PYTHONPATH, WorkingDirectory, ExecStart)
- [x] Created venv and installed dependencies (discord.py, etc.)
- [x] Added `__init__.py` to make `src` a proper package
- [x] Switched entry point to `python -m src.main` (modern event loop)
- [x] Service starts cleanly, state machine active, telemetry logging
- [x] Auto-approval for trades ≤ $250 (no Discord bot needed)

**Current Implementation:**
- `RpcIntegrator.execute_jupiter_trade()` now fully implemented with real Jupiter v6 API integration
- Jupiter API integration complete with wallet loading, quote retrieval, swap transaction, signing, and submission
- Implementation committed on branch `feature/126-meteora-dynamic-fees` (commit 2636457)

**Next Required Work:**
- [ ] **PR #148** for #134 (Jupiter implementation) is open; awaiting review/merge
- [ ] After merge: pull to ola-claw-trade and restart service
- [ ] Validate end-to-end: inject test signal, confirm Jupiter transaction
- [ ] Rotate exposed Jupiter API key (Pryan-Fire #143) **after** validation

**Owner:** Hugh the Hand (monitoring, testing, key rotation)

**Security Note:** Current Jupiter key exposed in chat — rotate once real Jupiter integration is tested.

---

## Pryan-Fire #134: Implement Real Jupiter Execution (IN PROGRESS)

**Objective:** Replace `RpcIntegrator.execute_jupiter_trade()` stub with actual Jupiter REST API calls to swap tokens on Solana.

**Status:** Implementation COMPLETE on branch `feature/126-meteora-dynamic-fees`. PR #148 created and open for review. GitHub issue: https://github.com/The-Nexus-Decoded/Pryan-Fire/issues/134

**Implementation details:**
- Loads wallet from `/data/openclaw/keys/trading_wallet.json` or `TRADING_WALLET_SECRET`
- Fetches quote via Jupiter v6 `/quote` endpoint (with fallback)
- Retrieves swap transaction via `/swap` endpoint
- Signs and submits transaction via Solana RPC
- Includes error handling, logging, retries via httpx

**Dependencies:** Pryan-Fire #141 (service infrastructure)

**Owner:** Haplo (implementation), Hugh (commit, PR, test)

**Next:** Review and merge by Zifnab; then pull to ola-claw-trade and validate.

---

## Pryan-Fire #145: Provision Trading Wallet Credentials (COMPLETED 2026-03-02)

**Objective:** Securely provision the trading wallet private key to ola-claw-trade after Jupiter API integration is complete and ready for testing.

**Status:** ✅ COMPLETED — Wallet file created at `/data/openclaw/keys/trading_wallet.json` (600 perms)

**Wallet address:** `74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x` (from MEMORY.md)

**Provisioned by:** Zifnab (coordination), key from Sterol

**Ready for:** End-to-end test after #134 (Jupiter impl) is deployed.

**Owner:** Hugh the Hand (validation)

---

## Pryan-Fire #143: Rotate Exposed Jupiter API Key (PENDING)

**Objective:** Generate new Jupiter API key and update `/data/openclaw/keys/jupiter-api-key` after real Jupiter integration is validated.

**Status:** Pending #134 test completion.

**Owner:** Hugh the Hand

---

## Wallet Analyzer Overnight Run (2026-03-02) ⏳ IN PROGRESS

**Objective:** Pull full transaction history for 3 wallets (owner, wallet2, bot) and generate position analysis reports.

**Status:** RUNNING as background process (PID 713874, nohup). NOT in tmux.

**Fixes applied by Lord Xar (2026-03-02 session 11):**
- Endpoint: `mainnet.helius-rpc.com` (was `api.helius.xyz/rpc` — wrong endpoint, caused 404 Method Not Found)
- User-Agent header added (was missing — caused Cloudflare 403/1010 block)
- `maxSupportedTransactionVersion: 0` added to getTransaction params (was missing — caused -32015 errors on all v0 txs)

**Configuration:**
- Helius API key: `/data/openclaw/workspace/Pryan-Fire/tools/solana-wallet-analyzer/.env`
- Wallets: Owner (`sh36vHUDHcXqVD8aZJR8GF3Z3PdaU69XG8wJeB1e1xb`), Wallet2 (`HZP3wFQd7nUu1V1WLXG9tau681qz165YVtrYhePDmqVW`), Bot (`74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x`)
- Output: `output/wallet_N/raw_transactions.json`
- Log: `output/pipeline.log`

**How to check status:** `tail -5 /data/openclaw/workspace/Pryan-Fire/tools/solana-wallet-analyzer/output/pipeline.log && ls -lh output/wallet_1/`

**Owner:** Hugh (monitoring)

**Restarted:** 2026-03-02 12:00 UTC

**Expected completion:** ~5 hours (587 pages, ~30 sec/page)

**Next:** Review reports; feed insights to trade signals.

---

## Chelestra-Sea #3 - Intelligence Database Query API (PENDING)

**Objective:** Build a FastAPI/Flask service to expose search and retrieval endpoints over the ChromaDB intelligence database (22,630 documents from Chelestra-Sea #2).

**Status:** PENDING (blocked on Jupiter functionality, not just service uptime)

**Dependencies:**
- Jupiter trading integration must be **functionally complete** (real API calls, not just service running)
- ChromaDB database fully built at `/data/intelligence/chroma/`
- SQLite metadata at `/data/intelligence/sqlite/`

**Planned endpoints:**
- `POST /search` – natural language query → top-k results
- `POST /similar` – document ID → similar documents
- `GET /report` – aggregated insights (thematic, temporal, entity extraction)

**Integration points:**
- Feed query results to `TradeOrchestrator` for position sizing and risk assessment
- Connect wallet analysis patterns to trading signals
- Support Hugh's market research workflow

**Owner:** Hugh the Hand (to be created after Jupiter validation)

**Related:** Chelestra-Sea #2 (completed), Pryan-Fire #141 (service running, functional Jupiter pending), Chelestra-Sea auth issues (#60, #63, #68) may affect GitHub workflows for this task.

---

## Chelestra-Sea Auth Issues (Blocking GitHub ops)

**Issues:** #60, #63, #68 (BRAVE_API_KEY, GitHub CLI auth, expired PAT)

These are assigned to Chelestra-Sea maintainer. They block intelligence query API development but not current orchestrator operation.

**Owner:** Chelestra-Sea maintainer

---

## Chelestra-Sea #3 - Intelligence Query API (2026-03-02) ✅ IN PROGRESS

**Objective:** Build a FastAPI service to expose search and retrieval endpoints over the ChromaDB/SQLite intelligence database (22,630 documents from Chelestra-Sea #2).

**Status:** IMPLEMENTATION COMPLETE — PR #82 open and ready for review.

**Implementation details:**
- Service built in `Chelestra-Sea/integrations/intelligence-api/`
- Endpoints: `POST /search`, `POST /similar`, `GET /report`
- Health checks: `/health`, `/ready`
- Connects to `/data/intelligence/owner-intelligence.db`
- Configurable via environment variables

**Testing:**
- Local test passed: server starts, connects to DB, returns results (total 24,088 documents)
- Query verified: `curl -X POST "http://127.0.0.1:8004/search?query=solana&limit=2"`

**Integration:**
- Pryan-Fire TradeOrchestrator will query this API for context enrichment
- Keeps separation: Chelestra-Sea provides infrastructure, Pryan-Fire consumes

**Next:**
- [ ] PR review and merge by Zifnab
- [ ] Deploy service on integration host (ola-claw-main or dedicated)
- [ ] Verify network connectivity from Pryan-Fire
- [ ] Integrate into TradeOrchestrator's signal processing
- [ ] Address extractions table population (currently empty — need to run structured extraction step)

**Owner:** Hugh the Hand (implementation), Zifnab (deployment coordination)