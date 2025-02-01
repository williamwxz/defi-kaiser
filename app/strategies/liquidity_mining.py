# app/strategies/liquidity_mining.py
class LiquidityMiningOptimizer:
    def __init__(self, min_tvl=500_000):
        self.min_tvl = min_tvl  # Minimum TVL to consider a pool

    def optimize(self, pools):
        """
        Select the best pool based on APR and TVL.
        """
        viable_pools = [p for p in pools if p['tvl'] >= self.min_tvl]
        if not viable_pools:
            return None
        
        # Score pools by APR adjusted for impermanent loss risk
        best_pool = max(viable_pools, key=lambda x: x['apr'] * (1 - x['il_risk']))
        return {
            'action': 'ADD_LIQUIDITY',
            'pool': best_pool['pair'],
            'amount': 0.2,  # 20% of capital
            'apr': best_pool['apr']
        }