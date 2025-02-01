# app/strategies.py
from pydantic import BaseModel

class TradeSignal(BaseModel):
    asset: str
    amount: float
    direction: str  # BUY/SELL
    chain: str = 'berachain'

class RWAArbitrage:
    def __init__(self, min_spread=0.015):
        self.min_spread = min_spread  # 1.5% minimum arbitrage
        
    def find_opportunities(self, rwa_yields, defi_rates):
        signals = []
        for asset, rwa_yield in rwa_yields.items():
            defi_rate = defi_rates.get('USDC', 0.045)  # Compare vs USDC
            spread = rwa_yield - defi_rate
            
            if spread > self.min_spread:
                signals.append(TradeSignal(
                    asset=asset,
                    amount=0.1,  # Risk-managed in execute.py
                    direction='BUY'
                ))
            elif spread < -self.min_spread:
                signals.append(TradeSignal(
                    asset=asset,
                    amount=0.1,
                    direction='SELL'
                ))
        return signals

class BerachainLPOptimizer:
    def optimize(self, pools, min_tvl=500_000):
        """Select pool with highest APR above TVL threshold"""
        viable = [p for p in pools if p['tvl'] >= min_tvl]
        if not viable:
            return None
        return max(viable, key=lambda x: x['apr'])