# app/data/processors.py
import numpy as np
from datetime import datetime
from typing import Dict, List
from .fetcher import PoolData

class DataProcessor:
    def __init__(self):
        self.stable_pairs = {'USDC', 'USDT', 'DAI'}

    def process_pools(self, pools: List[PoolData]) -> List[PoolData]:
        """Enrich pool data with derived metrics"""
        for pool in pools:
            # Calculate APR stability score
            pool.apr_stability = self._calculate_apr_stability(pool)
            
            # Calculate liquidity efficiency score
            pool.liquidity_score = self._calculate_liquidity_score(pool)
            
            # Add volatility estimate
            pool.volatility = self._estimate_volatility(pool)
            
            # Add risk-adjusted APR
            pool.risk_adjusted_apr = pool.apr * (1 - pool.il_risk)
            
        return sorted(pools, key=lambda x: x.risk_adjusted_apr, reverse=True)

    def _calculate_apr_stability(self, pool: PoolData) -> float:
        """Calculate APR stability based on fee/reward composition"""
        if pool.fee_apr and pool.reward_apr:
            return min(pool.fee_apr / (pool.fee_apr + pool.reward_apr), 1.0)
        return 1.0

    def _calculate_liquidity_score(self, pool: PoolData) -> float:
        """Calculate liquidity efficiency score"""
        volume_ratio = pool.volume_24h / max(pool.tvl, 1)
        return np.tanh(volume_ratio)  # Normalize between 0-1

    def _estimate_volatility(self, pool: PoolData) -> float:
        """Estimate volatility from IL risk and volume"""
        return min(pool.il_risk * 2 + (1 - self._calculate_liquidity_score(pool)), 1.0)

    def filter_pools(self, pools: List[PoolData], 
                    min_tvl: float = 100000,
                    max_il_risk: float = 0.3) -> List[PoolData]:
        """Filter pools based on quality criteria"""
        return [
            p for p in pools
            if p.tvl >= min_tvl
            and p.il_risk <= max_il_risk
            and not self._is_stable_pair(p.pair)
        ]

    def _is_stable_pair(self, pair: str) -> bool:
        """Check if pair contains only stablecoins"""
        a, b = pair.split('/')
        return a in self.stable_pairs and b in self.stable_pairs

    def normalize_rwa_data(self, rwa_data: Dict) -> Dict:
        """Normalize RWA data from multiple sources"""
        return {
            asset: {
                'price': data['price'],
                'yield': data['yield'],
                'score': data['yield'] * (1 - data.get('risk', 0.1)),
                'timestamp': datetime.utcnow().isoformat()
            }
            for asset, data in rwa_data.items()
        }