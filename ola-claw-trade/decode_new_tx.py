#!/usr/bin/env python3
import os, base64, json, httpx
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solders.pubkey import Pubkey

# Load wallet
with open('/data/openclaw/keys/trading_wallet.json') as f:
    secret = json.load(f)
kp = Keypair.from_bytes(bytes(secret))
wallet_pubkey = str(kp.pubkey())

# Get Jupiter transaction with SOL -> USDC
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

# Swap transaction payload
swap_url = f"{jupiter_endpoint}/swap"
payload = {
    "quoteResponse": quote,
    "userPublicKey": wallet_pubkey,
    "wrapAndUnwrapSol": True,
    "useSharedAccounts": False,
    "prioritizationFeeLamports": "auto"
}
resp = httpx.post(swap_url, json=payload, headers=headers, timeout=10.0)
resp.raise_for_status()
data = resp.json()
swap_tx_b64 = data.get("swapTransaction")
raw_tx = base64.b64decode(swap_tx_b64)

vt = VersionedTransaction.from_bytes(raw_tx)
msg = vt.message

print("=== Account keys ===")
for i, ak in enumerate(msg.account_keys):
    print(f"{i}: {ak}")

print("\n=== Instructions ===")
for i, ix in enumerate(msg.instructions):
    program_id = str(ix.program_id)
    accounts = [str(ak) for ak in ix.accounts]
    data_hex = ix.data.hex() if hasattr(ix, 'data') else "N/A"
    print(f"Instr {i}: program={program_id}")
    print(f"  Accounts: {accounts}")
    print(f"  Data: {data_hex[:40]}{'...' if len(data_hex)>40 else ''}")

print("\n=== Fee payer ===")
print("Account at index 0:", msg.account_keys[0])

print("\n=== Wallet in keys? ===")
print(wallet_pubkey in [str(ak) for ak in msg.account_keys])

# Check if USDC ATA (Associated Token Account for USDC) is included?
# The wallet's USDC ATA address is: (lookup via spl.* but we can compute)
# Associated token account program id: "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
# Derivation: PDA(seeds=["associated-token", mint, wallet]) program "ATokenGP..."
# Let's compute via spl.token?
from spl.token.constants import ASSOCIATED_TOKEN_PROGRAM_ID
from spl.publickey import PublicKey

def get_associated_token_address(owner: Pubkey, mint: Pubkey):
    return PublicKey.find_program_address(
        [bytes(PublicKey(owner)), bytes(PublicKey(ASSOCIATED_TOKEN_PROGRAM_ID)), bytes(PublicKey(mint))],
        PublicKey(ASSOCIATED_TOKEN_PROGRAM_ID)
    )[0]

owner = Pubkey.from_string(wallet_pubkey)
mint = Pubkey.from_string(output_mint)
ata = get_associated_token_address(owner, mint)
print("\n=== Wallet's USDC ATA ===")
print(ata)
print("ATA in account keys?", str(ata) in [str(ak) for ak in msg.account_keys])
