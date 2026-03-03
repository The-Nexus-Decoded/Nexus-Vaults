#!/usr/bin/env python3
import os, base64, json, httpx
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.message import Message
from solders.instruction import Instruction
from solana.rpc.api import Client

# Load wallet
with open('/data/openclaw/keys/trading_wallet.json') as f:
    secret = json.load(f)
kp = Keypair.from_bytes(bytes(secret))
wallet_pubkey = kp.pubkey()

# Get Jupiter transaction
jupiter_endpoint = "https://api.jup.ag/swap/v1"
jupiter_api_key = "47974572-434b-4cb9-a54b-cfa34584797a"
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
    "userPublicKey": str(wallet_pubkey),
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
vt = VersionedTransaction.from_bytes(raw_tx)
msg = vt.message

print("=== Transaction Instructions ===")
for i, ix in enumerate(msg.instructions):
    program_id = str(ix.program_id)
    data = ix.data.hex() if hasattr(ix, 'data') else "N/A"
    accounts = [str(acc) for acc in ix.accounts]
    print(f"Instr {i}: program={program_id}")
    print(f"  Accounts ({len(accounts)}): {accounts}")
    print(f"  Data (hex): {data[:32]}{'...' if len(data)>32 else ''}")
    print()

print("=== Account keys in transaction ===")
for i, ak in enumerate(msg.account_keys):
    print(f"{i}: {ak}")

# Try simulation with logged instruction trace?
client = Client("https://api.mainnet-beta.solana.com")
sigs = list(vt.signatures)
idx = msg.account_keys.index(wallet_pubkey)
sigs[idx] = kp.sign_message(bytes(msg))
signed_tx = VersionedTransaction.populate(msg, sigs)

# Simulate with logging
print("\n=== Simulating with RPC (to get logs) ===")
try:
    # Use simulate_transaction with config to return logs
    sim_resp = client._client.post(
        method="simulateTransaction",
        params=[
            base64.b64encode(bytes(signed_tx)).decode('utf-8'),
            {
                "sigVerify": False,  # skip signature verification to get instruction execution
                "commitment": "processed",
                "encoding": "base64",
                "accounts": None,
                "replaceReject": None
            }
        ],
        opts=None,
    )
    result = sim_resp
    # The raw response may contain logs, but we'll parse using the RPC response object if available.
    # Alternatively, use client.simulate_transaction method but it doesn't expose logs easily.
    print("Simulation raw result:", result)
except Exception as e:
    print("Simulation error:", e)
