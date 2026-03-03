#!/usr/bin/env python3
"""
Diagnostic: Execute a Jupiter trade flow but with sending patched to no-op.
This signs the transaction (private key used) but does NOT broadcast.
Safe for real wallet keys as long as you trust the machine.
"""
import sys
import json
import os
import logging
import base64
from unittest.mock import MagicMock

# Setup basic logging to see debug output
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s %(message)s')

# Paths
SERVICE_SRC = "/data/repos/Pryan-Fire/hughs-forge/services/trade-orchestrator/src"
if SERVICE_SRC not in sys.path:
    sys.path.insert(0, SERVICE_SRC)

WALLET_PATH = "/data/openclaw/keys/trading_wallet.json"

from core.rpc_integration import RpcIntegrator
from solders.keypair import Keypair

# Load wallet (needed for userPublicKey and signing)
with open(WALLET_PATH, "r") as f:
    secret_key = json.load(f)
wallet = Keypair.from_bytes(bytes(secret_key))
wallet_pubkey = str(wallet.pubkey())
print(f"Wallet public key: {wallet_pubkey}")

# Create RpcIntegrator with dry_run=False to load wallet and RPC client
rpc = RpcIntegrator(dry_run=False)

# Patch the Solana RPC client send methods to prevent actual on-chain submission
def mock_send_transaction(tx, opts=None):
    print("PATCH: send_transaction called (legacy) - skipping broadcast")
    # Return a mock result with a signature attribute
    return MagicMock(value="MOCK_SIGNATURE")

def mock_send_raw_transaction(raw_tx, opts=None):
    print("PATCH: send_raw_transaction called (versioned) - skipping broadcast")
    return MagicMock(value="MOCK_SIGNATURE")

rpc.client.send_transaction = mock_send_transaction
rpc.client.send_raw_transaction = mock_send_raw_transaction

# Also patch get_latest_blockhash to return something harmless
orig_get_latest_blockhash = rpc.client.get_latest_blockhash
def mock_get_latest_blockhash():
    print("PATCH: get_latest_blockhash called - returning dummy blockhash")
    # Return an object with .value.blockhash attribute
    class DummyBlockhash:
        blockhash = "dummy_blockhash"
    return MagicMock(value=DummyBlockhash())
rpc.client.get_latest_blockhash = mock_get_latest_blockhash

# Parameters
input_mint = "So11111111111111111111111111111111111111112"  # WSOL
output_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
amount_sol = 0.001
amount_lamports = int(amount_sol * (10**9))

print(f"\nExecuting Jupiter trade with dry_run=False but send methods patched.")
print(f"Amount: {amount_sol} SOL ({amount_lamports} lamports) -> USDC")

result = rpc.execute_jupiter_trade(
    token_address=output_mint,
    amount=amount_sol
)

print(f"\nResult: {result}")
print("Diagnostic complete. Check logs for 'Wallet pubkey not found' or 'Sending' messages.")
