Create the trading wallet credentials file on ola-claw-trade after Jupiter API integration (Pryan-Fire #145) is complete and ready for testing.

**Background:**
- The `patryn-trader` service requires a wallet private key to execute real on-chain trades via Jupiter.
- Wallet address (from MEMORY.md): `74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x`
- The Jupiter integration stub in `rpc_integration.py` must be replaced with actual API calls before the wallet can be used.

**Implementation Steps:**

1. Wait for Pryan-Fire #145 to be merged and deployed to ola-claw-trade.
2. Securely obtain the private key for the above wallet address.
3. Create JSON keyfile with 600 permissions:
   ```bash
   echo '{"wallet_address":"74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x","private_key":"<PRIVATE_KEY>"}' > /data/openclaw/keys/trading_wallet.json
   chmod 600 /data/openclaw/keys/trading_wallet.json
   ```
   Alternatively, set `TRADING_WALLET_SECRET` in the systemd service.
4. Restart `patryn-trader` service.
5. Perform a small test trade ($1 USDC → SOL) to verify on-chain execution.
6. Coordinate Jupiter API key rotation (Pryan-Fire #143) after successful test.

**Acceptance Criteria:**
- `/data/openclaw/keys/trading_wallet.json` exists with 600 permissions (or env var set)
- Service recognizes wallet and can quote/swap via Jupiter
- Test transaction confirms on-chain (Solana explorer)
- No wallet private keys exposed in logs or environment

**Notes:**
- Do NOT provision before #145 is deployed; stub code won't use it and would expose the key.
- After first real trade, rotate the exposed Jupiter API key from PR #142 (see #143).

**Blocks:** #145
