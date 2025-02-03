from pydantic import BaseModel
from typing import Dict
from cachetools import TTLCache, cached

class RWAArbitrageSignal(BaseModel):
    asset: str
    action: str  # "BUY_RWA" or "SELL_RWA"
    amount: float
    spread: float

class RWAArbitrageStrategy:
    def __init__(self, min_spread=0.015, max_position=0.1):
        self.min_spread = min_spread  # 1.5%
        self.max_position = max_position  # 10% of capital
        self.cache = TTLCache(maxsize=100, ttl=300)

    @cached(cache=TTLCache(maxsize=10, ttl=60))
    def get_opportunities(self, rwa_yields: Dict, defi_rates: Dict) -> list[RWAArbitrageSignal]:
        signals = []
        for asset, rwa_yield in rwa_yields.items():
            spread = rwa_yield - defi_rates.get('USDC', 0.045)
            
            if spread > self.min_spread:
                signals.append(RWAArbitrageSignal(
                    asset=asset,
                    action="BUY_RWA",
                    amount=self.max_position,
                    spread=spread
                ))
            elif spread < -self.min_spread:
                signals.append(RWAArbitrageSignal(
                    asset=asset,
                    action="SELL_RWA",
                    amount=self.max_position,
                    spread=abs(spread)
                ))
        return signals