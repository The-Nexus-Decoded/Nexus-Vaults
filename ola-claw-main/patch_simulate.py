import sys

def patch_simulate(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Replace simulate_rebalance
    start_idx = -1
    end_idx = -1
    for i, line in enumerate(lines):
        if "async def simulate_rebalance" in line:
            start_idx = i
        if start_idx != -1 and "log_telemetry" in line:
            end_idx = i + 5 # to get the closing brace
            break

    if start_idx != -1 and end_idx != -1:
        new_method = """    async def simulate_rebalance(self, position_data: Dict[str, Any], new_range: Dict[str, int], current_volatility: str = "NORMAL", dynamic_fees: Dict[str, Any] = None) -> Dict[str, Any]:
        \"\"\"Simulates a rebalance to provide a structured Flight Record.\"\"\"
        logger.info(f"--- [FLIGHT RECORDER: SIMULATED REBALANCE] ---")
        
        current_val = float(position_data.get("liquidity", 0))
        est_tx_fee = 0.005 # Total SOL for remove + add txs
        
        est_dust_loss = current_val * 0.0005
        est_slippage = current_val * 0.001
        
        base_expected_yield = current_val * 0.002 # Fallback
        if dynamic_fees:
            fee_rate = float(dynamic_fees.get("current_total_fee_rate", 20)) / 10000.0
            base_expected_yield = current_val * fee_rate * 5
            
        volatility_yield_multiplier = {"LOW": 0.5, "NORMAL": 1.0, "HIGH": 2.5}.get(current_volatility, 1.0)
        expected_fee_capture = base_expected_yield * volatility_yield_multiplier

        is_profitable = self.rebalance_strategy.check_profitability_threshold(expected_fee_capture, est_tx_fee + est_dust_loss, est_slippage)
        
        fee_capture_increase = 100 if (position_data['activeId'] < position_data['lowerBinId'] or position_data['activeId'] > position_data['upperBinId']) else 25 
        
        report = {
            "ESTIMATED_REBALANCE_COST": f"{(est_tx_fee + est_dust_loss + est_slippage):.5f} SOL",
            "EXPECTED_FEE_CAPTURE": f"{expected_fee_capture:.5f}",
            "PROJECTED_FEE_CAPTURE_INCREASE": f"{fee_capture_increase}%",
            "DUST_RESIDUE_ESTIMATE": f"{est_dust_loss:.6f} units",
            "RISK_MANAGER_STATUS": "APPROVED" if is_profitable else "VETOED"
        }
        log_telemetry("SIMULATED_REBALANCE", {
            "cost": (est_tx_fee + est_dust_loss + est_slippage),
            "expected_yield": expected_fee_capture,
            "projected_fee_increase": fee_capture_increase,
            "dust_estimate": est_dust_loss,
            "status": "APPROVED" if is_profitable else "VETOED"
        })
        
        return report, is_profitable
"""
        del lines[start_idx:end_idx+1]
        lines.insert(start_idx, new_method)
    
    with open(filepath, 'w') as f:
        f.writelines(lines)
    print("Patched simulate.")

patch_simulate('/data/openclaw/workspace/Pryan-Fire/hughs-forge/services/trade-executor/main.py')
