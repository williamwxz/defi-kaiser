# app/strategies/main.py
from cross_chain_arb import CrossChainArbitrage
from liquidity_mining import LiquidityMiningStrategy
from circuit_breaker import CircuitBreaker
from position_sizing import PositionSizer
from rwa_arbitrage import RWAArbitrageStrategy


class StrategyOrchestrator:
    def __init__(self):
        self.rwa_strategy = RWAArbitrageStrategy()
        self.liquidity_strategy = LiquidityMiningStrategy()
        self.circuit_breaker = CircuitBreaker()
        self.position_sizer = PositionSizer()


    def run_strategies(self, 
            rwa_yields: dict,
            defi_rates: dict,
            pools: list,
            portfolio: dict,
            market_data: dict):
        # Check market conditions first
        market_conditions = self.circuit_breaker.check_market_conditions(portfolio, market_data)
        if market_conditions.trading_halted:
            return []
        """
        Run all strategies and return aggregated signals.
        """
        signals = []

         # RWA Arbitrage
        rwa_signals = self.rwa_strategy.get_opportunities(rwa_yields, defi_rates)
        for signal in rwa_signals:
            signal.amount *= market_conditions.position_cap
            signals.append(signal)

        # Liquidity Mining
        liquidity_signals = self.liquidity_strategy.generate_signals(pools)
        for signal in liquidity_signals:
            signal.amount *= market_conditions.position_cap
            signals.append(signal)

        return signals