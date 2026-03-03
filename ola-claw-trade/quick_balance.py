#!/usr/bin/env python3
import sys, os, json, asyncio

# Add src to path (same as test_trade.py)
sys.path.insert(0, '/data/repos/Pryan-Fire/hughs-forge/services/trade-orchestrator/src')

from infrastructure.rpc_integration import RpcIntegrator

async def main():
    config = {
        "trading_wallet_public_key": os.getenv("TRADING_WALLET_PUBLIC_KEY", "74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x"),
        "rpc_url": "https://api.devnet.solana.com",
        "slippage_bps": 50,
    }
    rpc = RpcIntegrator(config)
    wallet = config["trading_wallet_public_key"]
    balance = await rpc.get_wallet_balance(wallet)
    print(json.dumps(balance, indent=2))

    # Also print SOL in lamports for accuracy
    from solana.rpc.api import Client
    from solana.publickey import PublicKey
    client = Client(config["rpc_url"])
    sol_balance = client.get_balance(PublicKey(wallet))
    print(f"SOT balance (lamports): {sol_balance}")

if __name__ == "__main__":
    asyncio.run(main())
