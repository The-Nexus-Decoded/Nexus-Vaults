#!/usr/bin/env python3
import json
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from spl.token.constants import ASSOCIATED_TOKEN_PROGRAM_ID

with open('/data/openclaw/keys/trading_wallet.json') as f:
    secret = json.load(f)
kp = Keypair.from_bytes(bytes(secret))
wallet = kp.pubkey()
usdc_mint = Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")

# Associated Token Account address
ata = Pubkey.find_program_address(
    [bytes(wallet), bytes(ASSOCIATED_TOKEN_PROGRAM_ID), bytes(usdc_mint)],
    ASSOCIATED_TOKEN_PROGRAM_ID
)[0]
print("Wallet:", wallet)
print("USDC mint:", usdc_mint)
print("ATA address:", ata)
