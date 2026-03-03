#!/usr/bin/env python3
"""
Diagnostic: Fetch Jupiter quote and swap transaction to inspect transaction structure.
This does NOT sign or send any transaction. Safe to run with real wallet pubkey.
"""
import sys
import json
import os
import logging

# Setup basic logging to see debug output
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s %(message)s')

# Paths
SERVICE_SRC = "/data/repos/Pryan-Fire/hughs-forge/services/trade-orchestrator/src"
if SERVICE_SRC not in sys.path:
    sys.path.insert(0, SERVICE_SRC)

WALLET_PATH = "/data/openclaw/keys/trading_wallet.json"

from core.rpc_integration import RpcIntegrator
from solders.keypair import Keypair

# Load wallet (we need the pubkey; we'll also load the keypair but won't use it to sign)
with open(WALLET_PATH, "r") as f:
    secret_key = json.load(f)
wallet = Keypair.from_bytes(bytes(secret_key))
wallet_pubkey = str(wallet.pubkey())
print(f"Wallet public key: {wallet_pubkey}")

# Create RpcIntegrator (dry_run=True prevents Solana client init; not needed)
rpc = RpcIntegrator(dry_run=True)

# Params
input_mint = "So11111111111111111111111111111111111111112"  # WSOL
output_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
amount_sol = 0.001
amount_lamports = int(amount_sol * (10**9))

print(f"\nFetching quote for {amount_sol} SOL -> USDC...")
quote = rpc._fetch_quote(
    input_mint=input_mint,
    output_mint=output_mint,
    amount=amount_lamports,
    user_public_key=wallet_pubkey
)
if not quote:
    print("ERROR: Failed to fetch quote")
    sys.exit(1)

print(f"Quote fetched. Output amount: {quote.get('outAmount')} USDC (in {quote.get('inAmount')} lamports)")
print(f"Quote routes: {len(quote.get('routes', []))} route(s)")

print("\nFetching swap transaction...")
swap_tx_b64 = rpc._fetch_swap_transaction(quote, wallet_pubkey)
if not swap_tx_b64:
    print("ERROR: Failed to fetch swap transaction")
    sys.exit(1)

print(f"Swap transaction base64 length: {len(swap_tx_b64)}")
print(f"First 200 chars: {swap_tx_b64[:200]}")

# Optionally decode and inspect transaction signers
try:
    import base64
    raw_tx = base64.b64decode(swap_tx_b64)
    # Determine format
    if raw_tx[0] in (0x80, 0x81):
        from solders.transaction import VersionedTransaction
        tx = VersionedTransaction.from_bytes(raw_tx)
        account_keys = [str(pk) for pk in tx.message.account_keys]
        print(f"\nVersionedTransaction accounts ({len(account_keys)}):")
        for i, pk in enumerate(account_keys):
            print(f"  {i}: {pk}")
        # Check if wallet is present
        if wallet_pubkey in account_keys:
            idx = account_keys.index(wallet_pubkey)
            print(f"\nWallet is present in account keys at index {idx}.")
        else:
            print(f"\nWallet {wallet_pubkey} is NOT in account keys!")
    else:
        from solders.transaction import Transaction
        tx = Transaction.from_bytes(raw_tx)
        account_keys = [str(pk) for pk in tx.message.account_keys]
        print(f"\nLegacy Transaction accounts ({len(account_keys)}):")
        for i, pk in enumerate(account_keys):
            print(f"  {i}: {pk}")
        if wallet_pubkey in account_keys:
            idx = account_keys.index(wallet_pubkey)
            print(f"\nWallet is present in account keys at index {idx}.")
        else:
            print(f"\nWallet {wallet_pubkey} is NOT in account keys!")
except Exception as e:
    print(f"Failed to decode transaction: {e}")

print("\nDiagnostic complete. No transaction was signed or sent.")
