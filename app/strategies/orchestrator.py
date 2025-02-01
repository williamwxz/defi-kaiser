# app/strategies/main.py
from cross_chain_arb import CrossChainArbitrage
from liquidity_mining import LiquidityMiningOptimizer

class StrategyOrchestrator:
    def __init__(self):
        self.rwa_arb = CrossChainArbitrage()
        self.lp_optimizer = LiquidityMiningOptimizer()

    def run_strategies(self, rwa_prices, bera_pools):
        """
        Run all strategies and return aggregated signals.
        """
        signals = []

        # Run RWA arbitrage
        rwa_signal = self.rwa_arb.find_opportunities(
            rwa_prices['OUSG'], 1.00, 0.005  # Underlying price = $1.00, fee = 0.5%
        )
        if rwa_signal:
            signals.append(rwa_signal)

        # Run liquidity mining optimization
        lp_signal = self.lp_optimizer.optimize(bera_pools)
        if lp_signal:
            signals.append(lp_signal)

        return signals