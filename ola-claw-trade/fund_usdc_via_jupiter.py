#!/usr/bin/env python3
"""Fund devnet wallet with USDC by swapping 0.1 SOL → USDC via Jupiter v6."""
import sys
import os
sys.path.insert(0, '/data/repos/Pryan-Fire/hughs-forge/services/trade-orchestrator/src')

from core.rpc_integration import RpcIntegrator

def main():
    print("[FUND] Initializing RpcIntegrator (dry_run=False)")
    integrator = RpcIntegrator(dry_run=False)
    # Check SOL balance first
    # integrator.wallet is loaded in __init__
    pubkey = integrator.wallet.pubkey() if integrator.wallet else None
    print(f"[FUND] Wallet: {pubkey}")
    # Get SOL balance via RPC
    try:
        balance_resp = integrator.client.get_balance(integrator.wallet.pubkey())
        sol_balance = balance_resp.value / 1e9
        print(f"[FUND] Current SOL balance: {sol_balance:.6f}")
    except Exception as e:
        print(f"[FUND] Warning: could not fetch SOL balance: {e}")
    # Execute SOL -> USDC swap
    input_mint = "So11111111111111111111111111111111111111112"  # Wrapped SOL
    output_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
    amount = 0.1  # SOL
    print(f"[FUND] Swapping {amount} SOL → USDC")
    success = integrator.execute_jupiter_trade(input_mint, amount)
    if success:
        print("[FUND] Swap transaction sent successfully.")
        # Optionally check USDC balance after a delay
        print("[FUND] Check wallet USDC balance manually or in subsequent test.")
    else:
        print("[FUND] Swap FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
