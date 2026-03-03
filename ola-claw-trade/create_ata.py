#!/usr/bin/env python3
import os, sys, json
from solana.publickey import Pubkey
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.transaction import Transaction
from spl.token.instructions import create_associated_token_account, get_associated_token_address

# Load wallet secret (list of ints)
with open('/data/openclaw/keys/trading_wallet.json') as f:
    secret = json.load(f)
secret_bytes = bytes(secret)
kp = Keypair.from_secret_key(secret_bytes)
wallet_pubkey = kp.public_key

# USDC mint on mainnet
usdc_mint = Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")

# Compute ATA address
ata = get_associated_token_address(wallet_pubkey, usdc_mint)
print(f"Creating USDC ATA: {ata}")

# Build instruction
instruction = create_associated_token_account(
    payer=wallet_pubkey,
    owner=wallet_pubkey,
    mint=usdc_mint
)

# Get recent blockhash
client = Client("https://api.mainnet-beta.solana.com")
blockhash_resp = client.get_latest_blockhash()
recent_blockhash = blockhash_resp.value.blockhash

# Build transaction
tx = Transaction()
tx.fee_payer = wallet_pubkey
tx.recent_blockhash = recent_blockhash
tx.add(instruction)

# Send with skip_preflight (idempotent)
try:
    result = client.send_transaction(
        tx,
        kp,
        opts=TxOpts(skip_preflight=True, skip_confirmation=False, max_retries=3)
    )
    print("ATA creation tx submitted:", result)
except Exception as e:
    print("ATA creation failed:", e)
    sys.exit(1)

# Wait and check
import time
time.sleep(8)
info = client.get_account_info(ata)
if info.value:
    print("✅ ATA created. Owner:", info.value.owner)
else:
    print("❌ ATA not yet visible. Check transaction status separately.")
