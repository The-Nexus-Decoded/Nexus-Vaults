#!/usr/bin/env python3
"""
Check wallet balance and fund USDC if needed via Jupiter swap (devnet).
Uses the same RpcIntegrator as the service -> correct endpoints.
"""
import asyncio
import json
import os
import sys
from pathlib import Path

# Add venv path
venv_python = Path("/data/repos/Pryan-Fire/hughs-forge/venv/bin/python")
if venv_python.exists():
    # Already running in venv? Assume we are.
    pass

from hughs_forge.rpc_integration import RpcIntegrator

async def main():
    # Load config from environment (same as service)
    config = {
        "owner_wallet_public_key": os.getenv("OWNER_WALLET_PUBLIC_KEY"),
        "trading_wallet_public_key": os.getenv("TRADING_WALLET_PUBLIC_KEY"),
        "private_key": os.getenv("SOLANA_PRIVATE_KEY"),  # for transaction signing
        "rpc_url": os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com"),
        "slippage_bps": 50,  # 0.5%
    }

    # Validate required keys
    required = ["trading_wallet_public_key", "private_key"]
    missing = [k for k in required if not config.get(k)]
    if missing:
        print(f"ERROR: Missing env vars: {missing}")
        sys.exit(1)

    rpc = RpcIntegrator(config)
    wallet = config["trading_wallet_public_key"]

    print(f"Checking balance for wallet: {wallet}")
    balance = await rpc.get_wallet_balance(wallet)
    print(f"Current balance: {balance}")

    usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # devnet USDC
    sol_balance = balance.get("SOL", 0.0)
    usdc_balance = balance.get(usdc_mint, 0.0)

    print(f"SOL: {sol_balance}, USDC: {usdc_balance}")

    # If we already have at least 0.5 USDC, no need to fund
    if usdc_balance >= 0.5:
        print("USDC balance sufficient. No funding needed.")
        sys.exit(0)

    # Need to fund: swap SOL -> USDC
    print("Insufficient USDC. Swapping 0.1 SOL to USDC...")

    # Perform the swap. Note: RpcIntegrator.execute_jupiter_trade swaps token->SOL by default.
    # We need SOL->USDC, so we must call with in_token=SOL mint, out_token=USDC mint.
    # The existing method expects input_token and output_token mints.
    # For SOL, the mint is "So11111111111111111111111111111111111111112".
    SOL_MINT = "So11111111111111111111111111111111111111112"

    result = await rpc.execute_jupiter_trade(
        input_token=SOL_MINT,
        output_token=usdc_mint,
        amount=0.1,  # SOL amount
        wallet_public_key=wallet
    )

    print("Swap result:")
    print(json.dumps(result, indent=2))

    if result.get("success"):
        print("✅ Funding swap successful. Transaction signature:", result.get("signature"))
        sys.exit(0)
    else:
        print("❌ Funding swap failed:", result.get("error"))
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
