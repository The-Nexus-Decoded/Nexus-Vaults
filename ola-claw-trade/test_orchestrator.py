#!/usr/bin/env python3
"""Test harness for TradeOrchestrator signal processing."""
import sys
import time
import json
import logging
from pathlib import Path

# Add src to path so we can import from the service package
SRC_PATH = "/data/repos/The-Nexus-Decoded/Pryan-Fire/hughs-forge/services/trade-orchestrator/src"
sys.path.insert(0, SRC_PATH)

from core.orchestrator import TradeOrchestrator
from core.event_loop import EventLoop
from telemetry.logger import setup_telemetry_logger

def main():
    # Setup telemetry to console
    logger = setup_telemetry_logger(log_file="test_orchestrator.jsonl")
    logger.info("Test harness starting", extra={"payload": {"test": "signal_injection"}})

    # Initialize orchestrator (uses trades.db by default)
    orchestrator = TradeOrchestrator(db_path="test_trades.db")
    event_loop = EventLoop(orchestrator)

    # Start event loop in background thread
    loop_thread = threading.Thread(target=event_loop.run, daemon=True, name="Test-Loop")
    loop_thread.start()
    time.sleep(0.5)  # Give loop time to start

    # Enqueue a test signal
    test_signal = {
        "trade_id": "TEST001",
        "token_address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyMs2tS",  # USDC
        "amount": 10.0,  # $10
        "action": "BUY",
        "source": "test_harness"
    }
    logger.info("Enqueuing test signal", extra={"payload": test_signal})
    event_loop.enqueue_signal(test_signal)

    # Wait for processing
    time.sleep(2.0)

    # Check state in DB
    state = orchestrator.state_manager.get_trade("TEST001")
    if state:
        logger.info("Trade state retrieved", extra={"payload": state})
        print("\n=== Trade State ===")
        print(json.dumps(state, indent=2))
    else:
        logger.error("Trade state not found in DB")
        print("ERROR: Trade state not found")

    # Stop event loop
    event_loop.stop()
    loop_thread.join(timeout=2.0)
    logger.info("Test harness complete")

if __name__ == "__main__":
    import threading
    main()
