import numpy as np

class PositionSizer:
    def __init__(self, max_capital_risk=0.1):
        self.max_capital_risk = max_capital_risk  # 10% of total capital
        
    def kelly_size(self, win_prob: float, win_loss_ratio: float) -> float:
        """Kelly Criterion position sizing"""
        kelly_f = (win_prob * win_loss_ratio - (1 - win_prob)) / win_loss_ratio
        return min(kelly_f, self.max_capital_risk)
        
    def volatility_adjusted_size(self, position_size: float, volatility: float) -> float:
        """Reduce position size in high volatility"""
        return position_size * np.exp(-volatility * 2)
