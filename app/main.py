# app/main.py
from data.fetcher import RWADataFetcher, Chain, DexDataFetcher
from strategies.orchestrator import StrategyOrchestrator
from execute import TradeExecutor
from risk.manager import RiskManager
import time

def trading_loop():
    rwa_fetcher = RWADataFetcher()
    dex_fetcher = DexDataFetcher()
    strategy_orchestrator = StrategyOrchestrator()
    executor = TradeExecutor()
    risk_manager = RiskManager()

    while True:
        try:
            # Step 1: Fetch data
            rwa_prices = rwa_fetcher.get_rwa_prices()
            bera_pools = dex_fetcher.get_dex_pools(Chain.BERACHAIN)

            # Step 2: Generate signals
            signals = strategy_orchestrator.run_strategies(rwa_prices, bera_pools)

            # Step 3: Execute trades
            for signal in signals:
                if risk_manager.approve_trade(signal):
                    if 'asset' in signal:  # RWA arbitrage trade
                        executor.execute_rwa_trade(signal)
                    elif 'pool' in signal:  # Liquidity mining trade
                        executor.execute_lp_trade(signal)

            # Cooldown period
            time.sleep(60)  # 1 min between iterations

        except Exception as e:
            print(f"Critical error: {e}")
            time.sleep(300)  # Backoff on failure

if __name__ == "__main__":
    trading_loop()