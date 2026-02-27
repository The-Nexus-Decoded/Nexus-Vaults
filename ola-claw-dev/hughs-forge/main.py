import os
import asyncio
from dotenv import load_dotenv
from solders.keypair import Keypair
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed

# --- Configuration ---
load_dotenv()

def get_config():
    """Loads and validates necessary configuration from environment variables."""
    rpc_endpoint = os.getenv("SOLANA_RPC_ENDPOINT")
    wallet_secret_key_b58 = os.getenv("DEVNET_WALLET_SECRET_KEY")

    if not rpc_endpoint:
        raise ValueError("SOLANA_RPC_ENDPOINT is not set in the .env file.")
    if not wallet_secret_key_b58:
        raise ValueError("DEVNET_WALLET_SECRET_KEY is not set in the .env file.")

    try:
        wallet_keypair = Keypair.from_base58_string(wallet_secret_key_b58)
    except Exception as e:
        raise ValueError(f"Invalid DEVNET_WALLET_SECRET_KEY: {e}")

    return {
        "rpc_endpoint": rpc_endpoint,
        "wallet_keypair": wallet_keypair,
    }

# --- Main Trading Logic ---
async def trading_loop(client: AsyncClient, wallet: Keypair):
    """The main loop for checking positions, claiming, and reinvesting."""
    print("Starting trading loop...")
    wallet_address = wallet.pubkey()
    print(f"Wallet address: {wallet_address}")

    # 1. Check RPC connection
    try:
        balance = await client.get_balance(wallet_address, commitment=Confirmed)
        print(f"Wallet balance: {balance.value / 1e9:.6f} SOL")
        print("RPC connection successful.")
    except Exception as e:
        print(f"Error connecting to RPC endpoint: {e}")
        return

    # --- Execute TypeScript Trading Logic ---
    # This script will handle the full cycle: fetch, claim, and reinvest.
    print("--- Bridging to TypeScript Execution Armory ---")
    ts_executor_path = "services/trade-executor"
    
    # Ensure the .env file is accessible to the Node process
    # The command inherits the environment from this Python script, and `load_dotenv` already loaded it.
    process = await asyncio.create_subprocess_exec(
        "npx", "ts-node", "src/main.ts",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=ts_executor_path
    )

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        print("--- TypeScript Executor finished successfully ---")
        if stdout:
            print(f"stdout:\n{stdout.decode()}")
    else:
        print(f"--- TypeScript Executor failed with exit code {process.returncode} ---")
        if stderr:
            print(f"stderr:\n{stderr.decode()}")
        if stdout:
            print(f"stdout:\n{stdout.decode()}")
    
    print("Trading loop finished.")

# --- Entry Point ---
async def main():
    """Main function to initialize and run the trading bot."""
    print("Initializing Solana Trading Bot for Hugh...")
    try:
        config = get_config()
        print(f"Connecting to RPC endpoint: {config['rpc_endpoint']}")
        
        async with AsyncClient(config["rpc_endpoint"], commitment=Confirmed) as client:
            await trading_loop(client, config["wallet_keypair"])

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
