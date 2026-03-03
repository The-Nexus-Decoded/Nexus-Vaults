#!/usr/bin/env python3
import os, httpx, json
from decimal import Decimal

jupiter_endpoint = "https://api.jup.ag/swap/v1"
jupiter_api_key = "47974572-434b-4cb9-a54b-cfa34584797a"

# Test with 0.01 SOL (10,000,000 lamports)
input_mint = "So11111111111111111111111111111111111111112"  # wSOL
output_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC (6 decimals)
amount_lamports = 10_000_000

params = {
    "inputMint": input_mint,
    "outputMint": output_mint,
    "amount": str(amount_lamports),
    "slippageBps": "50",
    "onlyDirectRoutes": "false"
}
headers = {"User-Agent": "OpenClaw-Haplo/1.0", "x-api-key": jupiter_api_key}

resp = httpx.get(f"{jupiter_endpoint}/quote", params=params, headers=headers, timeout=10.0)
resp.raise_for_status()
quote = resp.json()

print("Quote response (excerpt):")
print(json.dumps(quote, indent=2)[:1000])

# Parse output amount
if "outAmount" in quote:
    out_amount_raw = int(quote["outAmount"])
    # USDC has 6 decimals
    out_amount_usdc = Decimal(out_amount_raw) / (10**6)
    print(f"\nInput: {amount_lamports} lamports = {amount_lamports/1e9:.6f} SOL")
    print(f"Output raw: {out_amount_raw} base units")
    print(f"Output USDC: {out_amount_usdc:.6f} USDC")
else:
    print("No outAmount in quote")
