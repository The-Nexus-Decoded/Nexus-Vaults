#!/usr/bin/env python3
import asyncio
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solana.rpc.commitment import Confirmed

RPC_URL = "https://api.devnet.solana.com"
WALLET = "74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x"

async def check_and_airdrop():
    client = Client(RPC_URL)
    pubkey = Pubkey.from_string(WALLET)
    # Check balance
    bal = client.get_balance(pubkey, commitment=Confirmed)
    lamports = bal.value
    sol = lamports / 1_000_000_000
    print(f"Current balance: {lamports} lamports ({sol} SOL)")

    if lamports >= 500_000_000:  # 0.5 SOL should be enough
        print("Sufficient SOL already. No airdrop needed.")
        return True

    # Need SOL: try airdrop up to 3 times
    for attempt in range(3):
        try:
            print(f"Airdrop attempt {attempt+1}/3: requesting 1 SOL...")
            resp = client.request_airdrop(pubkey, 1_000_000_000, commitment=Confirmed)
            sig = resp["result"]
            print(f"Signature: {sig}")
            # Wait a bit for confirmation
            import time
            time.sleep(5)
            client.confirm_transaction(sig, commitment=Confirmed)
            # Recheck balance
            bal = client.get_balance(pubkey, commitment=Confirmed)
            lamports = bal.value
            sol = lamports / 1_000_000_000
            print(f"Post-airdrop balance: {lamports} lamports ({sol} SOL)")
            return lamports >= 500_000_000
        except Exception as e:
            print(f"Airdrop attempt {attempt+1} failed: {e}")
            if attempt < 2:
                import time
                time.sleep(5)
            else:
                print("All airdrop attempts failed.")
                return False

if __name__ == "__main__":
    success = asyncio.run(check_and_airdrop())
    exit(0 if success else 1)
