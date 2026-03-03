#!/usr/bin/env python3
import json, httpx, time
from solana.rpc.api import Client

sig = "deCD6GWRRB3EszPGRddXjWNJwz7h9HCmjLsQNdW6cyn5QM9CMMguiUHrWw6Pcsn4LSfxZVynU6tX2GyUi8mMwLa"
client = Client("https://api.mainnet-beta.solana.com")

# Poll for up to 30 seconds
for i in range(12):
    try:
        resp = client.get_signature_statuses([sig])
        status = resp.value[0]
        if status:
            print(f"Status: {status.confirmation_status}")
            if status.err:
                print(f"Error: {status.err}")
            else:
                print(f"Confirmed at slot: {status.slot}")
                # Fetch transaction details
                tx = client.get_transaction(sig, encoding="jsonParsed")
                print(json.dumps(tx.value.to_json(), indent=2)[:2000])
                break
        else:
            print(f"Not yet confirmed (attempt {i+1})...")
            time.sleep(5)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
else:
    print("Timeout: transaction not confirmed within 30s.")
