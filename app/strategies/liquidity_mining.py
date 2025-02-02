from typing import List
from models import Chain, PoolData, LiquidityAction, LiquiditySignal

class LiquidityMiningStrategy:
    def __init__(self, min_tvl=500_000, max_il_risk=0.3):
        self.min_tvl = min_tvl
        self.max_il_risk = max_il_risk
        self.chain_weights = {
            Chain.BERACHAIN: 0.5,  # Higher weight for Berachain
            Chain.ETHEREUM: 0.3,
            Chain.POLYGON: 0.15,
            Chain.BSC: 0.05
        }

    def generate_signals(self, pools: List[PoolData]) -> List[LiquiditySignal]:
        """
        Generate liquidity signals for multiple chains.
        """
        signals = []
        
        # Filter viable pools
        viable_pools = [
            p for p in pools
            if p.tvl >= self.min_tvl and p.il_risk <= self.max_il_risk
        ]
        
        if not viable_pools:
            return signals
            
        # Score pools: 60% APR, 40% volume/TVL ratio
        scored_pools = sorted(
            viable_pools,
            key=lambda x: (0.6 * x.apr) + (0.4 * (x.volume_24h / x.tvl)),
            reverse=True
        )
        
        # Allocate capital based on chain weights
        for chain, weight in self.chain_weights.items():
            chain_pools = [p for p in scored_pools if p.chain == chain]
            if not chain_pools:
                continue
                
            # Top 2 pools per chain
            for pool in chain_pools[:2]:
                signals.append(LiquiditySignal(
                    chain=pool.chain,
                    pair=pool.pair,
                    action=LiquidityAction.ADD_LIQUIDITY,
                    amount=weight * 0.5  # 50% of chain allocation
                ))
            
        # Remove liquidity from risky pools
        for pool in [p for p in pools if p.il_risk > self.max_il_risk]:
            signals.append(LiquiditySignal(
                chain=pool.chain,
                pair=pool.pair,
                action=LiquidityAction.REMOVE_LIQUIDITY,
                amount=1.0  # 100% of position
            ))
            
        return signals