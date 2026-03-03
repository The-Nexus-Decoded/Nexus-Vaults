#!/usr/bin/env python3
"""Direct SOL -> USDC swap on devnet using Jupiter v6 api.jup.ag/swap/v1."""
import os, json, httpx, base64
from solders.keypair import Keypair
from solana.rpc.api import Client
from solders.transaction import VersionedTransaction
from solders.signature import Signature
from solana.rpc.types import TxOpts

# Config
WALLET_PATH = "/data/openclaw/keys/trading_wallet.json"
RPC_URL = "https://api.devnet.solana.com"
QUOTE_URL = "https://api.jup.ag/swap/v1/quote"
SWAP_URL = "https://api.jup.ag/swap/v1/swap"
INPUT_MINT = "So11111111111111111111111111111111111111112"  # SOL
OUTPUT_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
AMOUNT_SOL = 0.1
SLIPPAGE_BPS = 50

def main():
    # Load wallet
    with open(WALLET_PATH) as f:
        secret = json.load(f)
    kp = Keypair.from_bytes(bytes(secret))
    print(f"[INFO] Wallet: {kp.pubkey()}")

    # Jupiter API key
    api_key = os.getenv("JUPITER_API_KEY")
    if not api_key:
        with open("/data/openclaw/keys/jupiter.env") as f:
            for line in f:
                if "=" in line:
                    k,v=line.strip().split("=",1)
                    if k=="JUPITER_API_KEY": api_key=v; break
    if not api_key:
        print("ERROR: JUPITER_API_KEY missing")
        return
    headers = {"x-api-key": api_key, "User-Agent": "OpenClaw-Hugh/1.0"}

    amount_lamports = int(AMOUNT_SOL * 1_000_000_000)
    print(f"[INFO] Swapping {AMOUNT_SOL} SOL → USDC")

    # Quote
    params = {
        "inputMint": INPUT_MINT,
        "outputMint": OUTPUT_MINT,
        "amount": str(amount_lamports),
        "slippageBps": SLIPPAGE_BPS,
    }
    resp = httpx.get(QUOTE_URL, params=params, headers=headers, timeout=15.0)
    if resp.status_code != 200:
        print(f"[ERROR] Quote failed {resp.status_code}: {resp.text[:200]}")
        return
    quote = resp.json()
    print(f"[INFO] Quote: outAmount={quote.get('outAmount')}, priceImpactPct={quote.get('priceImpactPct')}%")

    # Swap transaction
    payload = {
        "quoteResponse": quote,
        "userPublicKey": str(kp.pubkey()),
        "wrapAndUnwrapSol": True,
        "useSharedAccounts": False,
        "prioritizationFeeLamports": "auto"
    }
    resp2 = httpx.post(SWAP_URL, json=payload, headers=headers, timeout=15.0)
    if resp2.status_code != 200:
        print(f"[ERROR] Swap request failed {resp2.status_code}: {resp2.text[:200]}")
        return
    swap_data = resp2.json()
    swap_tx_b64 = swap_data.get("swapTransaction")
    if not swap_tx_b64:
        print("[ERROR] No swapTransaction in response")
        return
    print("[INFO] Swap transaction obtained")

    # Deserialize, sign, send
    raw_tx = base64.b64decode(swap_tx_b64)
    client = Client(RPC_URL)
    try:
        tx = VersionedTransaction.from_bytes(raw_tx)
        msg = tx.message
        sigs = list(tx.signatures)
        account_keys = msg.account_keys
        try:
            idx = account_keys.index(kp.pubkey())
        except ValueError:
            print("[ERROR] Wallet pubkey not in tx")
            return
        signature = kp.sign_message(bytes(msg))
        if idx < len(sigs):
            sigs[idx] = signature
        else:
            print(f"[ERROR] Sig index {idx} out of bounds")
            return
        signed_tx = VersionedTransaction.populate(msg, sigs)
        print("[INFO] Sending transaction...")
        result = client.send_raw_transaction(bytes(signed_tx), opts=TxOpts(skip_confirmation=False, preflight_commitment="processed"))
        tx_hash = str(result.value)
        print(f"[SUCCESS] Tx signature: {tx_hash}")
    except Exception as e:
        print(f"[ERROR] Send failed: {e}")
        return

if __name__ == "__main__":
    main()
