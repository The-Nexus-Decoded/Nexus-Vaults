import sys

def patch_strategy(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    # Replace profitability_check with check_profitability_threshold
    start_idx = -1
    end_idx = -1
    for i, line in enumerate(lines):
        if "def profitability_check" in line:
            start_idx = i
        if start_idx != -1 and "return is_profitable" in line:
            end_idx = i
            break
            
    if start_idx != -1 and end_idx != -1:
        new_method = """    def check_profitability_threshold(self, expected_fee_capture: float, estimated_swap_gas: float, potential_slippage: float) -> bool:
        \"\"\"
        Checks if the rebalance is financially viable.
        Requires expected fee capture to be greater than the cost of rebalancing.
        \"\"\"
        total_friction = estimated_swap_gas + potential_slippage
        is_profitable = expected_fee_capture > total_friction 
        
        logger.info(f"--> Profitability Threshold Check: Expected Capture: {expected_fee_capture:.5f}, Total Friction: {total_friction:.5f} (Gas: {estimated_swap_gas:.5f}, Slippage: {potential_slippage:.5f}). Approved: {is_profitable}")
        
        return is_profitable
"""
        del lines[start_idx:end_idx+1]
        lines.insert(start_idx, new_method)
    
    with open(filepath, 'w') as f:
        f.writelines(lines)
    print("Patched strategy.")

patch_strategy('/data/openclaw/workspace/Pryan-Fire/hughs-forge/services/trade-executor/main.py')
