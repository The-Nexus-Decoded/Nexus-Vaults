#!/usr/bin/env python3
import os, base64, json, httpx
from solders.transaction import VersionedTransaction
from solders.pubkey import Pubkey

# Config
jupiter_endpoint = "https://api.jup.ag/swap/v1"
jupiter_api_key = os.getenv("JUPITER_API_KEY", "")
user_pubkey = "74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x"
input_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
output_mint = "So11111111111111111111111111111111111111112"
amount_lamports = 1000000  # 0.001 SOL

# Step 1: Get quote
quote_url = f"{jupiter_endpoint}/quote"
params = {
    "inputMint": input_mint,
    "outputMint": output_mint,
    "amount": str(amount_lamports),
    "slippageBps": "50",
    "onlyDirectRoutes": "false"
}
headers = {"User-Agent": "OpenClaw-Haplo/1.0"}
if jupiter_api_key:
    headers["x-api-key"] = jupiter_api_key

resp = httpx.get(quote_url, params=params, headers=headers, timeout=10.0)
resp.raise_for_status()
quote = resp.json()
print("Quote fetched. Routes:", quote.get("routes", [])[:1])

# Step 2: Get swap transaction
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
if not swap_tx_b64:
    raise Exception("No swapTransaction in response")
print("Swap transaction base64 length:", len(swap_tx_b64))

# Decode and inspect
raw_tx = base64.b64decode(swap_tx_b64)
try:
    vt = VersionedTransaction.from_bytes(raw_tx)
    msg = vt.message
    account_keys = [str(ak) for ak in msg.account_keys]
    print("VersionedTransaction account keys:")
    for i, ak in enumerate(account_keys):
        print(f"  {i}: {ak}")
    print("Num signatures:", len(vt.signatures))
    print("Fee payer index (first):", 0)
    print("Wallet in keys?:", Pubkey.from_string(user_pubkey) in msg.account_keys)
except Exception as e:
    print("Failed to deserialize as VersionedTransaction:", e)
    try:
        from solana.transaction import Transaction as LegacyTransaction
        lt = LegacyTransaction.from_bytes(raw_tx)
        print("Legacy Transaction account keys:", [str(ak) for ak in lt.message.account_keys])
    except Exception as e2:
        print("Also failed as legacy:", e2)
