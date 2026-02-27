import asyncio
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.rpc.types import MemcmpOpts
import json
import base64

METEORA_DLMM_PROGRAM_ID = Pubkey.from_string("LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo")
BOT_WALLET_PUBKEY = Pubkey.from_string("74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x")
RPC_ENDPOINT = "https://api.mainnet-beta.solana.com" 

def test():
    client = Client(RPC_ENDPOINT)
    
    print(f"DEBUG: Using raw Client.get_program_accounts...")
    
    try:
        # Test 1: Minimal filter
        memcmp_filter = MemcmpOpts(offset=8, bytes=str(BOT_WALLET_PUBKEY))
        
        print("Calling get_program_accounts...")
        # Note: calling the synchronous version for simplicity in this test
        response = client.get_program_accounts(
            METEORA_DLMM_PROGRAM_ID,
            filters=[memcmp_filter]
        )
        
        print(f"Success! Found {len(response.value)} accounts.")
            
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()
