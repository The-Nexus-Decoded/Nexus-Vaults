#!/usr/bin/env python3
import os, base64, json
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.message import Message
from solders.signature import Signature

# Load wallet
with open('/data/openclaw/keys/trading_wallet.json') as f:
    secret = json.load(f)
kp = Keypair.from_bytes(bytes(secret))
print("Wallet pubkey:", str(kp.pubkey()))

# Load the raw transaction from the debug script's hypothetical cache; we need the actual raw_tx and signature
# Instead, we'll reproduce the steps: get the raw transaction from Jupiter and sign it, then verify.

import httpx

jupiter_endpoint = "https://api.jup.ag/swap/v1"
jupiter_api_key = "47974572-434b-4cb9-a54b-cfa34584797a"
user_pubkey = str(kp.pubkey())
input_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
output_mint = "So11111111111111111111111111111111111111112"
amount_lamports = 1000000

# Quote
quote_url = f"{jupiter_endpoint}/quote"
params = {
    "inputMint": input_mint,
    "outputMint": output_mint,
    "amount": str(amount_lamports),
    "slippageBps": "50",
    "onlyDirectRoutes": "false"
}
headers = {"User-Agent": "OpenClaw-Haplo/1.0", "x-api-key": jupiter_api_key}
resp = httpx.get(quote_url, params=params, headers=headers, timeout=10.0)
resp.raise_for_status()
quote = resp.json()

# Swap transaction
swap_url = f"{jupiter_endpoint}/swap"
payload = {
    "quoteResponse": quote,
    "userPublicKey": user_pubkey,
    "wrapAndUnwrapSol": True,
    "useSharedAccounts": False,
    "prioritizationFeeLamports": "auto"
}
resp = httpx.post(swap_url, json=payload, headers=headers, timeout=10.0)
resp.raise_for_status()
data = resp.json()
swap_tx_b64 = data.get("swapTransaction")
raw_tx = base64.b64decode(swap_tx_b64)

# Deserialize
from solders.transaction import VersionedTransaction
vt = VersionedTransaction.from_bytes(raw_tx)
msg = vt.message
message_bytes = bytes(msg)

# Sign
signature = kp.sign_message(message_bytes)
print("Signature:", signature)

# Verify locally
pubkey = kp.pubkey()
is_valid = signature.verify(pubkey, message_bytes)
print("Signature valid?", is_valid)

# Also check that the signature is present in the transaction after replacement
from solders.transaction import VersionedTransaction
sigs = list(vt.signatures)
idx = msg.account_keys.index(pubkey)
sigs[idx] = signature
signed_tx = VersionedTransaction.populate(msg, sigs)
print("Signed tx has correct signature?", signed_tx.signatures[idx].verify(pubkey, message_bytes))

# Try to simulate with RPC? Could attempt a dry-run via simulate or send with skip_confirmation? Let's try simulate_transaction
from solana.rpc.api import Client
client = Client("https://api.mainnet-beta.solana.com")
try:
    # simulate_transaction expects a transaction and signers
    # The method is client.simulate_transaction(transaction, signers=None, ...)
    # We'll pass signed_tx and no additional signers because it's already signed.
    sim = client.simulate_transaction(signed_tx)
    print("Simulation result:", sim.value.err)
except Exception as e:
    print("Simulation failed:", e)