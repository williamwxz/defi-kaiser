class ExecutionRiskManager:
    def __init__(self):
        self.max_slippage = 0.03  # 3%
        
    def validate_swap(self, order_size: float, pool_liquidity: float) -> bool:
        liquidity_impact = order_size / pool_liquidity
        return liquidity_impact * 0.5 <= self.max_slippage
        
    def get_optimal_gas(self, chain_state: dict) -> int:
        """Gas optimization for Berachain"""
        base_gas = chain_state['base_fee']
        if chain_state['pending_txs'] > 1000:
            return int(base_gas * 1.25)
        return int(base_gas * 0.9)