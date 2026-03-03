#!/usr/bin/env python3
"""
Debug script: Trace Jupiter API key loading and request headers in RpcIntegrator.
Does NOT modify any service files. Standalone diagnostic.
"""
import sys
import os
import logging

# Ensure we're using the workspace code
workspace = "/data/openclaw/workspace/Pryan-Fire"
sys.path.insert(0, f"{workspace}/hughs-forge/services/trade-orchestrator/src")
sys.path.insert(0, f"{workspace}/src")

# Set up logging to see internal messages
logging.basicConfig(level=logging.DEBUG, format='[%(name)s] %(levelname)s: %(message)s')

# Force the environment to match the service (will read from systemd env via os.getenv)
# But we can also print what the env actually contains
print("[*] Environment check:")
print(f"    JUPITER_API_KEY: {os.getenv('JUPITER_API_KEY', '(not set)')[:8] if os.getenv('JUPITER_API_KEY') else '(not set)'}")
print(f"    TRADING_WALLET_PATH: {os.getenv('TRADING_WALLET_PATH', '(not set)')}")
print(f"    SOLANA_RPC_URL: {os.getenv('SOLANA_RPC_URL', '(not set)')}")

# Now import and instantiate RpcIntegrator
try:
    from core.rpc_integration import RpcIntegrator
    print("[*] Creating RpcIntegrator instance (dry_run=True for safety)...")
    rpc = RpcIntegrator(dry_run=True)
    print(f"[*] rpc.jupiter_api_key: {rpc.jupiter_api_key[:8] if rpc.jupiter_api_key else '(None)'}")
except Exception as e:
    print(f"[!] Failed to import or instantiate RpcIntegrator: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Perform a direct quote fetch using the same internal method
print("\n[*] Testing _fetch_quote directly with debug logging...")
try:
    quote = rpc._fetch_quote(
        input_mint="So11111111111111111111111111111111111111112",
        output_mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        amount=1000000,  # 0.001 SOL lamports
        user_pubkey="74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x",
        slippage_bps=50
    )
    if quote:
        print(f"\n[SUCCESS] Quote fetched: inAmount={quote.get('inAmount')}, outAmount={quote.get('outAmount')}")
    else:
        print("\n[FAIL] _fetch_quote returned None")
except Exception as e:
    print(f"\n[ERROR] Exception during _fetch_quote: {e}")
    import traceback
    traceback.print_exc()
