#!/usr/bin/env python3
import os, base64, json, httpx
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction

# Load wallet
with open('/data/openclaw/keys/trading_wallet.json') as f:
    secret = json.load(f)
kp = Keypair.from_bytes(bytes(secret))

# Get Jupiter transaction (with updated mints: input wSOL, output USDC)
jupiter_endpoint = "https://api.jup.ag/swap/v1"
jupiter_api_key = "47974572-434b-4cb9-a54b-cfa34584797a"
input_mint = "So11111111111111111111111111111111111111112"  # wSOL
output_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
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
payload = {
    "quoteResponse": quote,
    "userPublicKey": str(kp.pubkey()),
    "wrapAndUnwrapSol": True,
    "useSharedAccounts": False,
    "prioritizationFeeLamports": "auto"
}
resp = httpx.post(f"{jupiter_endpoint}/swap", json=payload, headers=headers, timeout=10.0)
resp.raise_for_status()
swap_tx_b64 = resp.json().get("swapTransaction")
raw_tx = base64.b64decode(swap_tx_b64)

vt = VersionedTransaction.from_bytes(raw_tx)
msg = vt.message
sigs = list(vt.signatures)
idx = msg.account_keys.index(kp.pubkey())
sigs[idx] = kp.sign_message(bytes(msg))
signed_tx = VersionedTransaction.populate(msg, sigs)

# Simulate with sigVerify false
rpc_url = "https://api.mainnet-beta.solana.com"
jsonrpc_payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "simulateTransaction",
    "params": [
        base64.b64encode(bytes(signed_tx)).decode('utf-8'),
        {
            "sigVerify": False,
            "commitment": "processed",
            "encoding": "base64",
            "accounts": None
        }
    ]
}
resp = httpx.post(rpc_url, json=jsonrpc_payload, headers={"Content-Type": "application/json"}, timeout=30)
result = resp.json()
print(json.dumps(result, indent=2))
