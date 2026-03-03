import os
from solana.rpc.api import Client
from solders.keypair import Keypair
import json

wallet_path = os.getenv("TRADING_WALLET_PATH", "/data/openclaw/keys/trading_wallet.json")
with open(wallet_path) as f:
    secret = json.load(f)
kp = Keypair.from_bytes(bytes(secret))
client = Client("https://api.mainnet-beta.solana.com")
bal_resp = client.get_balance(kp.pubkey())
print("Balance type:", type(bal_resp))
print("Balance (lamports):", bal_resp.value if hasattr(bal_resp, 'value') else bal_resp)
print("Balance (SOL):", (bal_resp.value if hasattr(bal_resp, 'value') else bal_resp) / 1e9)
