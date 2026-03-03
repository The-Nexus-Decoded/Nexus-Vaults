#!/usr/bin/env python3
import os, base64, json, httpx, time
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solana.rpc.api import Client
from solana.rpc.types import TxOpts

# Load wallet
with open('/data/openclaw/keys/trading_wallet.json') as f:
    secret = json.load(f)
kp = Keypair.from_bytes(bytes(secret))
wallet_pubkey = str(kp.pubkey())
print("Wallet:", wallet_pubkey)

# Jupiter config
jupiter_endpoint = "https://api.jup.ag/swap/v1"
jupiter_api_key = "47974572-434b-4cb9-a54b-cfa34584797a"
input_mint = "So11111111111111111111111111111111111111112"
output_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
amount_sol = 0.001
amount_lamports = int(amount_sol * 1_000_000_000)
print(f"Swapping {amount_sol} SOL -> USDC")

headers = {"User-Agent": "OpenClaw-Haplo/1.0", "x-api-key": jupiter_api_key}

# Quote
quote_url = f"{jupiter_endpoint}/quote"
params = {
    "inputMint": input_mint,
    "outputMint": output_mint,
    "amount": str(amount_lamports),
    "slippageBps": "50",
    "onlyDirectRoutes": "false"
}
resp = httpx.get(quote_url, params=params, headers=headers, timeout=10.0)
resp.raise_for_status()
quote = resp.json()

# Swap transaction
payload = {
    "quoteResponse": quote,
    "userPublicKey": wallet_pubkey,
    "wrapAndUnwrapSol": True,
    "useSharedAccounts": False,
    "prioritizationFeeLamports": "auto"
}
resp = httpx.post(f"{jupiter_endpoint}/swap", json=payload, headers=headers, timeout=10.0)
resp.raise_for_status()
swap_tx_b64 = resp.json().get("swapTransaction")
if not swap_tx_b64:
    raise Exception("No swapTransaction")
raw_tx = base64.b64decode(swap_tx_b64)

# Sign
vt = VersionedTransaction.from_bytes(raw_tx)
msg = vt.message
sigs = list(vt.signatures)
idx = msg.account_keys.index(kp.pubkey())
sigs[idx] = kp.sign_message(bytes(msg))
signed_tx = VersionedTransaction.populate(msg, sigs)

# Send with skip_preflight and skip_confirmation to minimize RPC
client = Client("https://api.mainnet-beta.solana.com")
for attempt in range(1, 4):
    try:
        print(f"Attempt {attempt}: sending (no preflight, no confirm)...")
        result = client.send_raw_transaction(
            bytes(signed_tx),
            opts=TxOpts(skip_preflight=True, skip_confirmation=True)
        )
        print("SENT! Signature:", result.value)
        print("Check manually later. Exiting.")
        break
    except Exception as e:
        print(f"Send failed: {e}")
        if "429" in str(e) and attempt < 3:
            wait = 30 * attempt
            print(f"Rate limited. Retrying in {wait}s...")
            time.sleep(wait)
        else:
            print("Giving up.")
            raise