# Active Tasks

Ongoing crons, recurring jobs, multi-session projects.
Each task gets its own section. Archive completed tasks, don't delete.

---

## Volatility-Aware Rebalancing Implementation (Pryan-Fire #122)
Status: MERGED. PR #132 merged successfully (CI passed). Feature deployed via CI/CD. All sub-issues (#126-#131) closed automatically. GitHub App auth setup completed on ola-claw-dev (Chelestra-Sea #34) and ola-claw-trade (#35). Push auth issue (#48) resolved.
Last Updated: 2026-03-02

## CI/CD Deployment Pipeline (Pryan-Fire #1)
Status: Active, monitoring for workflow runs.
Last Updated: 2026-03-01

## P&L tracking (fees - IL - gas) (Pryan-Fire #14)
Status: COMPLETED. Implemented `TradeLedger` for P&L tracking, including recording trade entries and calculating overall realized P&L with robust handling of `None` values. Integrated into `TradeExecutor` and demonstrated via `main_async`.
Last Updated: 2026-03-01

## Ensure hughs-forge is correctly deployed/synced to Hugh's workspace (Chelestra-Sea #37)
Status: COMPLETED. The hughs-forge repository has been successfully synced to Hugh's workspace on ola-claw-trade, excluding virtual environments and node modules. All source code, configs, and scripts are deployed.
Last Updated: 2026-03-01

## Acquire Testnet SOL for Hugh's Devnet Testing (Pryan-Fire #125)
Status: COMPLETED. Approved by Lord Xar (issue CLOSED). Hugh to execute faucet claim.
Last Updated: 2026-03-02

## GitHub Authentication Issues (Nexus-Vaults #10, Chelestra-Sea #34, #35, #48)
Status: RESOLVED. All GitHub App auth setups completed, push operations verified. These issues were blocking PR merges and deployments. Closed 2026-03-02.
Last Updated: 2026-03-02

## Volatility-Aware Rebalancing (Pryan-Fire #122)
Status: DEPLOYED. PR #132 merged 2026-03-02T05:24:36Z. CI/CD deployment queued automatically (3 workflow runs: Patryn Trader MVP, Trade Executor, Trading Services).
Last Updated: 2026-03-02

## Hugh's Devnet Funding (Pryan-Fire #125)
Status: FUNDING APPROVED. Issue CLOSED by Lord Xar. Hugh to claim 5 SOL testnet from faucet (captcha expected) and verify deployment completion.
Last Updated: 2026-03-02

## Infra Pending (Unassigned)
- Chelestra-Sea #22: Browser tool failure (gateway token mismatch)
- Chelestra-Sea #27: Agent 'sessions: self failed' error
- Chelestra-Sea #17, #18, #19, #21: Various infra improvements (context pruning, Death Gate workflows, rate guard, Zifnab workflows)
These are pending assignment but NOT blocking current work.
Last Updated: 2026-03-02

## Fleet Protocol: Claude-Opus 4.6 Bypass Integration (Nexus-Vaults #12)
Status: Assigned to Haplo, secondary priority. BLOCKED: Awaiting passwordless SSH configuration to Windows Workstation. Monitoring for resolution.
Last Updated: 2026-03-01

## Fleet Protocol: Multi-Session Claude Code Orchestration (Nexus-Vaults #11)
Status: Research in progress. Documented OpenClaw ACP capabilities and current system state (only Pi CLI installed, no ACP config). Created research document at `/data/openclaw/workspace/research-multi-session-claude-code.md`. Next: test ACP spawning with Pi, check Discord ACP settings.
Last Updated: 2026-03-01

## Created Lobster Templates for Token Reduction (Nexus-Vaults #9)
Status: COMPLETED. All 6 templates implemented and pushed to Nexus-Vaults main:
- `haplo-build-test.lobster`
- `haplo-create-pr.lobster`
- `haplo-deploy-service.lobster`
- `zifnab-memory-maintenance.lobster`
- `zifnab-github-issue-creation.lobster`
- `zifnab-agent-restart.lobster`
Tracking issue Nexus-Vaults #13 remains open for future workflow additions.
Last Updated: 2026-03-02

## GitHub PAT Issue: Unable to Update Issues (olalawal account) (Nexus-Vaults #10)
Status: CLOSED (Duplicate of Chelestra-Sea #40, which is now resolved for Haplo's assignments).
Last Updated: 2026-03-01

## CRITICAL: Zifnab-bot GitHub PAT lacks permissions to assign issues (Chelestra-Sea #40)
Status: CLOSED (Resolved for Haplo's assignments, but Zifnab's self-assignment still has issues).
Last Updated: 2026-03-01

## Fleet Security & Cost Monitoring: Install Skill Vetter and Model Usage (Pryan-Fire #94)
Status: CLOSED by Lord Xar's directive (Sterol). Model usage and cost optimization work discontinued.
Last Updated: 2026-03-01

## Memory-Guard Service (Nexus-Vaults #14)
Status: COMPLETED. Created systemd user service unit (`memory-guard.service`) and enabled on `ola-claw-dev`. Service is active, watching MEMORY.md for changes, validating, backing up, and syncing to Nexus-Vaults. Initial backup and git push succeeded.
Last Updated: 2026-03-02

## Cron: health-check (ID: a8b9375f-3ad9-441a-8e65-6ad9e93866a0)
Status: COMPLETED. Gateway OK, disk usage 4%, Ollama OK. No alerts triggered.
Last Updated: 2026-03-01 21:44

## Current Session Notes (2026-03-02)
- Closed duplicate tracking issues: Chelestra-Sea #66, #67 (duplicate of #68).
- Verified lobster templates (Nexus-Vaults #9) already exist in repo and are functional; no further action needed.
- Implemented and deployed memory-guard systemd service on ola-claw-dev (Nexus-Vaults #14).
- Runner re-registration still pending (GitHub PAT lacks `Administration:write`; need elevated token or App key).

## Jupiter API Integration for Real Trading (Pryan-Fire #147)
Status: NOT STARTED. Assigned to Haplo. This is the critical path blocker for all trading operations.
- Issue Link: https://github.com/The-Nexus-Decoded/Pryan-Fire/issues/147
- Must implement `execute_jupiter_trade()` in `rpc_integration.py` using Jupiter v6 API
- Requires: wallet credentials (blocked on #145), Jupiter API key handling
- Service stub currently logs and returns True without on-chain activity
Last Updated: 2026-03-02

## Provision Trading Wallet Credentials (Pryan-Fire #145)
Status: BLOCKED (waiting for Jupiter integration #147). Assigned to HughTheHand.
- Issue Link: https://github.com/The-Nexus-Decoded/Pryan-Fire/issues/145
- Create `/data/openclaw/keys/trading_wallet.json` with 600 permissions after Jupiter integration deployed
- Wallet address: `74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x`
- Private key held by Sterol; secure provisioning required
- Must NOT provision before Jupiter integration (#147) is deployed or key will be exposed unnecessarily
Last Updated: 2026-03-02
