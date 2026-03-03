#!/usr/bin/env python3
import os, base64, json, httpx
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solana.rpc.api import Client
from solana.rpc.types import TxOpts

# Load wallet
with open('/data/openclaw/keys/trading_wallet.json') as f:
    secret = json.load(f)
kp = Keypair.from_bytes(bytes(secret))

# Get Jupiter transaction (SOL -> USDC)
jupiter_endpoint = "https://api.jup.ag/swap/v1"
jupiter_api_key = "47974572-434b-4cb9-a54b-cfa34584797a"
input_mint = "So11111111111111111111111111111111111111112"
output_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
amount_lamports = 1000000

# Quote and swap
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

swap_url = f"{jupiter_endpoint}/swap"
payload = {
    "quoteResponse": quote,
    "userPublicKey": str(kp.pubkey()),
    "wrapAndUnwrapSol": True,
    "useSharedAccounts": False,
    "prioritizationFeeLamports": "auto"
}
resp = httpx.post(swap_url, json=payload, headers=headers, timeout=10.0)
resp.raise_for_status()
swap_tx_b64 = resp.json().get("swapTransaction")
raw_tx = base64.b64decode(swap_tx_b64)

vt = VersionedTransaction.from_bytes(raw_tx)
msg = vt.message
sigs = list(vt.signatures)
idx = msg.account_keys.index(kp.pubkey())
sigs[idx] = kp.sign_message(bytes(msg))
signed_tx = VersionedTransaction.populate(msg, sigs)

# Send with skip_preflight and skip_confirmation
client = Client("https://api.mainnet-beta.solana.com")
try:
    result = client.send_raw_transaction(
        bytes(signed_tx),
        opts=TxOpts(skip_preflight=True, skip_confirmation=True)
    )
    print("Send result (skip_preflight):", result)
except Exception as e:
    print("Send failed:", e)
