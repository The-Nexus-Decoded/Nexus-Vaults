#!/usr/bin/env python3
"""One-off script: Swap 0.1 SOL → USDC on devnet via Jupiter v6 to fund test wallet."""
import os
import json
import httpx
import base64
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solders.transaction import VersionedTransaction
from solders.signature import Signature
from solana.rpc.types import TxOpts

# Config
WALLET_PATH = "/data/openclaw/keys/trading_wallet.json"
RPC_URL = "https://api.devnet.solana.com"
JUPITER_QUOTE_URL = "https://quote-api.jup.ag/v6/quote"
JUPITER_SWAP_URL = "https://quote-api.jup.ag/v6/swap"
INPUT_MINT = "So11111111111111111111111111111111111111112"  # Wrapped SOL
OUTPUT_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
AMOUNT_SOL = 0.1
SLIPPAGE_BPS = 50

def main():
    # Load wallet
    with open(WALLET_PATH, "r") as f:
        secret_key = json.load(f)
    kp = Keypair.from_bytes(bytes(secret_key))
    print(f"[INFO] Wallet pubkey: {kp.pubkey()}")

    # Jupiter API key
    jupiter_api_key = os.getenv("JUPITER_API_KEY")
    if not jupiter_api_key:
        env_path = "/data/openclaw/keys/jupiter.env"
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line=line.strip()
                    if line and not line.startswith("#"):
                        k,v=line.split("=",1)
                        if k=="JUPITER_API_KEY":
                            jupiter_api_key=v
                            break
    if not jupiter_api_key:
        print("[ERROR] JUPITER_API_KEY not found")
        return
    print("[INFO] Jupiter API key loaded")

    # Amount in lamports
    amount_lamports = int(AMOUNT_SOL * 1_000_000_000)
    print(f"[INFO] Swapping {AMOUNT_SOL} SOL ({amount_lamports} lamports) → USDC")

    # Get quote
    params = {
        "inputMint": INPUT_MINT,
        "outputMint": OUTPUT_MINT,
        "amount": str(amount_lamports),
        "slippageBps": SLIPPAGE_BPS,
    }
    headers = {"x-api-key": jupiter_api_key, "User-Agent": "OpenClaw-Hugh/1.0"}
    resp = httpx.get(JUPITER_QUOTE_URL, params=params, headers=headers, timeout=10.0)
    if resp.status_code != 200:
        print(f"[ERROR] Quote failed {resp.status_code}: {resp.text[:200]}")
        return
    quote = resp.json()
    print(f"[INFO] Quote received: outAmount={quote.get('outAmount')}")

    # Get swap transaction
    payload = {
        "quoteResponse": quote,
        "userPublicKey": str(kp.pubkey()),
        "wrapAndUnwrapSol": True,
        "useSharedAccounts": False,
        "prioritizationFeeLamports": "auto"
    }
    resp2 = httpx.post(JUPITER_SWAP_URL, json=payload, headers=headers, timeout=10.0)
    if resp2.status_code != 200:
        print(f"[ERROR] Swap transaction request failed {resp2.status_code}: {resp2.text[:200]}")
        return
    swap_data = resp2.json()
    swap_tx_b64 = swap_data.get("swapTransaction")
    if not swap_tx_b64:
        print("[ERROR] No swapTransaction in response")
        return
    print("[INFO] Swap transaction fetched")

    # Deserialize, sign, send
    raw_tx = base64.b64decode(swap_tx_b64)
    client = Client(RPC_URL)
    try:
        tx = VersionedTransaction.from_bytes(raw_tx)
        print("[INFO] Deserialized as VersionedTransaction")
        msg = tx.message
        sigs = list(tx.signatures)
        account_keys = msg.account_keys
        try:
            idx = account_keys.index(kp.pubkey())
        except ValueError:
            print("[ERROR] Wallet pubkey not found in tx account keys")
            return
        message_bytes = bytes(msg)
        signature = kp.sign_message(message_bytes)
        if idx < len(sigs):
            sigs[idx] = signature
        else:
            print(f"[ERROR] Sig index {idx} out of bounds")
            return
        signed_tx = VersionedTransaction.populate(msg, sigs)
        print("[INFO] Transaction signed, sending...")
        result = client.send_raw_transaction(bytes(signed_tx), opts=TxOpts(skip_confirmation=False, preflight_commitment="processed"))
        tx_hash = str(result.value)
        print(f"[SUCCESS] Transaction sent. Signature: {tx_hash}")
        # Verify USDC balance via Jupiter or RPC (optional)
    except Exception as e:
        print(f"[ERROR] Transaction send failed: {e}")
        return

if __name__ == "__main__":
    main()
