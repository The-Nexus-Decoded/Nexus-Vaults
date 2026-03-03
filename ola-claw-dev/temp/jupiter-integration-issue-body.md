Implement the Jupiter Aggregator v6 API within `hughs-forge/services/trade-orchestrator/src/rpc_integration.py` to enable real on-chain swaps and LP position management for Meteora DLMM.

**Background:**
- The current `rpc_integration.py` contains a stub for `execute_jupiter_trade()` and `get_meteora_dynamic_fees()`.
- Real trading operations require full integration with Jupiter's quote, swap, and transaction submission endpoints.
- This is a critical path item for activating Hugh's trading strategies.

**Implementation Steps:**

1.  **Jupiter Client Initialization:** Initialize the Jupiter v6 API client, including any necessary API keys (Pryan-Fire #140).
2.  **Quote Retrieval:** Implement functionality to get real-time swap quotes from Jupiter.
3.  **Swap Execution:** Implement secure transaction construction, signing (using wallet from #145), and submission for Jupiter swaps.
4.  **DLMM Position Management (Optional for initial MVP):** Research and implement logic for opening/closing Meteora DLMM positions via Jupiter where applicable.
5.  **Error Handling & Retries:** Implement robust error handling, including transaction failure retries and slippage protection.
6.  **Unit Tests:** Develop comprehensive unit tests for Jupiter API interactions.

**Acceptance Criteria:**
-   `execute_jupiter_trade()` successfully executes a test swap on devnet.
-   `get_meteora_dynamic_fees()` returns actual dynamic fee data from Meteora.
-   Code is modular, testable, and adheres to `hughs-forge` conventions.
-   No private keys are exposed in the codebase or logs.

**Notes:**
-   This issue is a prerequisite for "Provision Trading Wallet Credentials" (Pryan-Fire #145).
-   Coordinate API key procurement with Zifnab (Pryan-Fire #140).
