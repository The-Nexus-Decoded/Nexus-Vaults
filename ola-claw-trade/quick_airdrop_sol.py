#!/usr/bin/env python3
import asyncio
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solana.rpc.commitment import Confirmed

RPC_URL = "https://api.devnet.solana.com"
WALLET = "74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x"  # trading wallet

async def airdrop():
    client = Client(RPC_URL)
    pubkey = Pubkey.from_string(WALLET)
    # Request 1 SOL (1_000_000_000 lamports)
    print(f"Requesting airdrop of 1 SOL to {WALLET}...")
    try:
        resp = client.request_airdrop(pubkey, 1_000_000_000, commitment=Confirmed)
        sig = resp["result"]
        print(f"Airdrop initiated. Signature: {sig}")
        # Wait for confirmation
        client.confirm_transaction(sig, commitment=Confirmed)
        print("Airdrop confirmed.")
        # Check final balance
        bal = client.get_balance(pubkey, commitment=Confirmed)
        print(f"Final balance (lamports): {bal['result']['value']}")
    except Exception as e:
        print(f"Airdrop failed: {e}")

if __name__ == "__main__":
    asyncio.run(airdrop())
