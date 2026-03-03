#!/usr/bin/env python3
"""
Step 1: Pull transactions for configured wallets.

This script fetches recent transaction signatures for each configured wallet
and then retrieves the full transaction details, saving them as JSON files
in the corresponding output directory.

Configuration:
- Edit WALLETS below to map wallet IDs to Solana addresses.
- RPC endpoint can be set via SOLANA_RPC_URL environment variable; defaults to mainnet.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List

# Solana libraries
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("pull_transactions")

# Wallet mapping: {id: address_string}
WALLETS = {
    "wallet_1": "74QXtqTiM9w1D9WM8ArPEggHPRVUWggeQn3KxvR4ku5x",  # Bot wallet (example)
    "wallet_2": "sh36vHUDHcXqVD8aZJR8GF3Z3PdaU69XG8wJeB1e1xb",  # Owner wallet (example)
    "wallet_3": "INSERT_WALLET_3_ADDRESS_HERE"
}

# How many recent signatures to fetch per wallet
MAX_SIGNATURES = 100

def ensure_dirs():
    """Create output directories if they don't exist."""
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "output"
    for wid in WALLETS.keys():
        (output_dir / wid).mkdir(parents=True, exist_ok=True)
    return output_dir

def get_rpc_client() -> Client:
    rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    return Client(rpc_url)

def fetch_signatures(client: Client, wallet_pubkey: Pubkey, limit: int = MAX_SIGNATURES) -> List[Dict]:
    """Fetch recent transaction signatures for the given wallet."""
    try:
        resp = client.get_signatures_for_address(wallet_pubkey, limit=limit)
        if resp.value:
            return resp.value
        else:
            logger.warning(f"No signatures found for {wallet_pubkey}")
            return []
    except Exception as e:
        logger.error(f"Error fetching signatures for {wallet_pubkey}: {e}")
        return []

def fetch_transaction(client: Client, signature: str):
    """Fetch transaction details by signature."""
    try:
        resp = client.get_transaction(signature, encoding="json", max_supported_transaction_version=0)
        if resp.value:
            return resp.value
        else:
            logger.warning(f"Transaction {signature} not found")
            return None
    except Exception as e:
        logger.error(f"Error fetching transaction {signature}: {e}")
        return None

def save_transaction(output_dir: Path, wallet_id: str, signature: str, tx_data):
    """Save transaction data to a JSON file."""
    filename = output_dir / wallet_id / f"{signature}.json"
    try:
        with open(filename, 'w') as f:
            json.dump(tx_data, f, indent=2)
        logger.info(f"Saved transaction {signature} to {filename}")
    except Exception as e:
        logger.error(f"Failed to save transaction {signature}: {e}")

def main():
    logger.info("Starting wallet transaction pull")
    output_dir = ensure_dirs()
    client = get_rpc_client()
    
    for wallet_id, address in WALLETS.items():
        logger.info(f"Processing wallet {wallet_id}: {address}")
        wallet_pubkey = Pubkey.from_string(address)
        signatures_info = fetch_signatures(client, wallet_pubkey)
        
        if not signatures_info:
            continue
        
        logger.info(f"Fetched {len(signatures_info)} signatures for {wallet_id}")
        
        for sig_info in signatures_info:
            signature = sig_info.signature
            logger.debug(f"Fetching transaction {signature}")
            tx_data = fetch_transaction(client, signature)
            if tx_data:
                save_transaction(output_dir, wallet_id, signature, tx_data)
    
    logger.info("Transaction pull complete")

if __name__ == "__main__":
    main()
