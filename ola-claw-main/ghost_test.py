import asyncio
from decimal import Decimal
from src.executor.state_machine import TradeStateMachine, ExecutorState
from src.executor.kill_switch import KILL_SWITCH

async def ghost_run():
    print("--- INITIATING GHOST EXECUTION TEST ---")
    
    executor = TradeStateMachine()
    
    # 1. Test Small Opportunity (Within $250)
    print("\n[TEST 1] Small Opportunity (0.1 SOL -> ~$15)")
    small_op = {
        "input_mint": "So11111111111111111111111111111111111111112",
        "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "amount_atoms": 100000000, 
        "description": "SOL/USDC Small Test"
    }
    await executor.process_opportunity(small_op)

    # 2. Test Large Opportunity (Exceeds $250)
    print("\n[TEST 2] Large Opportunity (10 SOL -> ~$1500)")
    large_op = {
        "input_mint": "So11111111111111111111111111111111111111112",
        "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "amount_atoms": 10000000000, # 10 SOL
        "description": "SOL/USDC Large Threshold Test"
    }
    await executor.process_opportunity(large_op)
    
    print("\n--- GHOST TEST COMPLETE ---")

if __name__ == "__main__":
    try:
        asyncio.run(ghost_run())
    except KeyboardInterrupt:
        pass
