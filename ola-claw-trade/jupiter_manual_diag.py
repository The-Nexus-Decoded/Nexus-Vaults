#!/usr/bin/env python3
"""
Diagnostic: Manual Jupiter trade steps with detailed inspection.
"""
import sys
import json
import os
import logging
import base64

sys.path.insert(0, '/data/repos/Pryan-Fire/hughs-forge/services/trade-orchestrator/src')

from core.rpc_integration import RpcIntegrator
from solders.keypair import Keypair
from solders.transaction import Transaction, VersionedTransaction

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

WALLET_PATH = "/data/openclaw/keys/trading_wallet.json"
with open(WALLET_PATH) as f:
    secret_key = json.load(f)
wallet = Keypair.from_bytes(bytes(secret_key))
wallet_pubkey = str(wallet.pubkey())
print(f"Wallet: {wallet_pubkey}")

# RPC integrator (dry_run=False loads wallet and client)
rpc = RpcIntegrator(dry_run=False)

# Patch send methods to avoid broadcast
class MockResult:
    def __init__(self):
        self.value = "MOCK_SIGNATURE"
def mock_send_transaction(*args, **kwargs):
    print("PATCH: send_transaction -> skip")
    return MockResult()
def mock_send_raw_transaction(*args, **kwargs):
    print("PATCH: send_raw_transaction -> skip")
    return MockResult()
rpc.client.send_transaction = mock_send_transaction
rpc.client.send_raw_transaction = mock_send_raw_transaction
def mock_get_latest_blockhash():
    class Dummy: blockhash = "dummy"
    return type("M", (), {"value": Dummy()})()
rpc.client.get_latest_blockhash = mock_get_latest_blockhash

# Params
input_mint = "So11111111111111111111111111111111111111112"
output_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
amount_sol = 0.001
amount_lamports = int(amount_sol * (10**9))

print("\n=== Manual flow ===")
quote = rpc._fetch_quote(input_mint, output_mint, amount_lamports, user_public_key=wallet_pubkey)
if not quote:
    raise SystemExit("Quote failed")
print(f"Quote outAmount: {quote.get('outAmount')}")

swap_tx_b64 = rpc._fetch_swap_transaction(quote, wallet_pubkey)
if not swap_tx_b64:
    raise SystemExit("Swap tx fetch failed")
print(f"Swap tx base64 len: {len(swap_tx_b64)}")

raw_tx = base64.b64decode(swap_tx_b64)
print(f"Raw tx len: {len(raw_tx)}")
print(f"First 32 bytes hex: {raw_tx[:32].hex()}")
# Print around the signature/message boundary (offset 60-80)
print(f"Bytes 60-80 hex: {raw_tx[60:80].hex()}")
print(f"First byte: {raw_tx[0]} (hex: {hex(raw_tx[0])})")

# Try versioned
if raw_tx[0] in (0x80, 0x81):
    print("First byte indicates versioned transaction.")
    try:
        tx = VersionedTransaction.from_bytes(raw_tx)
        print("Deserialized as VersionedTransaction")
        # Continue with signing steps if desired...
    except Exception as e:
        print(f"VersionedTransaction.from_bytes error: {e}")
else:
    print("First byte is not 0x80/0x81, trying legacy Transaction.")
    try:
        tx = Transaction.from_bytes(raw_tx)
        print("Deserialized as legacy Transaction")
        # Inspect account keys
        accts = [str(pk) for pk in tx.message.account_keys]
        print(f"Account keys ({len(accts)}):")
        for i, pk in enumerate(accts):
            if pk == wallet_pubkey:
                print(f"  {i}: {pk} <--- WALLET HERE")
            else:
                print(f"  {i}: {pk}")
        if wallet_pubkey in accts:
            print("Wallet is present in account keys.")
        else:
            print("Wallet NOT found in account keys!")
    except Exception as e:
        print(f"Transaction.from_bytes error: {e}")
        with open("/tmp/failed_tx.bin", "wb") as f:
            f.write(raw_tx)
        print("Raw tx saved to /tmp/failed_tx.bin for analysis.")
