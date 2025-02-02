from models import MarketConditions

class CircuitBreaker:
    def __init__(self):
        self.max_drawdown = 0.25  # 25%
        self.volatility_threshold = 0.15  # 15% daily
        
    def check_market_conditions(self, portfolio, market_data) -> MarketConditions:
        conditions = MarketConditions(
            trading_halted=False,
            position_cap=1.0
        )
        
        # Drawdown check
        if portfolio.drawdown > self.max_drawdown:
            conditions.trading_halted = True
            
        # Volatility check
        if market_data['volatility'] > self.volatility_threshold:
            conditions.position_cap = 0.5  # Reduce positions by 50%
            
        return conditions