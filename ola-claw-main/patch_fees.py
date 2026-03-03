import sys

def insert_code(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    insert_idx = -1
    for i, line in enumerate(lines):
        if "async def get_meteora_lp_positions" in line:
            insert_idx = i
            break
            
    if insert_idx == -1:
        print("Target not found")
        return
        
    new_method = """    async def get_meteora_dynamic_fees(self, pool_pubkey: Pubkey) -> Dict[str, Any]:
        \"\"\"Fetches dynamic fee parameters for a Meteora DLMM Pool.\"\"\"
        logger.info(f"Fetching Dynamic Fees for {pool_pubkey}...")
        try:
            pool_data = await self.meteora_dlmm_program.account["Pool"].fetch(pool_pubkey)
            
            # Extract base_fee_rate and variable_fee_rate.
            base_fee_rate = getattr(pool_data, "base_fee_rate", getattr(pool_data, "fee_rate", 0))
            variable_fee_rate = getattr(pool_data, "variable_fee_rate", getattr(pool_data, "max_fee_rate", 0))
            
            current_total_fee_rate = base_fee_rate + variable_fee_rate
            
            logger.info(f"--> Dynamic Fees Decoded for {pool_pubkey}: Base: {base_fee_rate}, Variable: {variable_fee_rate}, Total: {current_total_fee_rate}")
            
            return {
                "base_fee_rate": base_fee_rate,
                "variable_fee_rate": variable_fee_rate,
                "current_total_fee_rate": current_total_fee_rate,
                "fee_tier_distribution": None
            }
        except Exception as e:
            logger.error(f"--> Error fetching Dynamic Fees for {pool_pubkey}: {e}")
            return {
                "base_fee_rate": 0,
                "variable_fee_rate": 0,
                "current_total_fee_rate": 0,
                "fee_tier_distribution": None
            }

"""
    lines.insert(insert_idx, new_method)
    
    with open(filepath, 'w') as f:
        f.writelines(lines)
    print("Patched.")

insert_code('/data/openclaw/workspace/Pryan-Fire/hughs-forge/services/trade-executor/main.py')
