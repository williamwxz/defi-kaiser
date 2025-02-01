# app/risk.py
class RiskManager:
    def __init__(self, capital=10_000):
        self.capital = capital
        self.max_position = 0.1  # 10% of capital
        self.min_tvl = 1_000_000  # Avoid illiquid pools
        
    def approve_trade(self, signal, pool_data=None):
        # Position size check
        if signal.amount > self.max_position * self.capital:
            return False
            
        # Liquidity check for DEX trades
        if pool_data and pool_data['tvl'] < self.min_tvl:
            return False
            
        return True