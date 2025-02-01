# app/risk/manager.py
class RiskManager:
    def __init__(self, capital=10_000):
        self.capital = capital
        self.max_position = 0.1  # 10% of capital per trade
        self.min_tvl = 500_000   # Minimum TVL for liquidity pools

    def approve_trade(self, signal):
        """
        Check if a trade is within risk limits.
        """
        # Position size check
        if signal['amount'] > self.max_position * self.capital:
            return False

        # Liquidity check for LP trades
        if 'pool' in signal and signal.get('tvl', 0) < self.min_tvl:
            return False

        return True

    def check_market_conditions(self, volatility, liquidity):
        """
        Halt trading during extreme market conditions.
        """
        if volatility > 0.1 or liquidity < 1_000_000:
            return False
        return True