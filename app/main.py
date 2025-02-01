# app/main.py
from data import DataFetcher
from strategies import RWAArbitrage, BerachainLPOptimizer, TradeSignal
from execute import TradeExecutor
import time

def trading_loop():
    fetcher = DataFetcher()
    rwa_arb = RWAArbitrage()
    lp_optimizer = BerachainLPOptimizer()
    executor = TradeExecutor()
    
    while True:
        try:
            # Step 1: Fetch data
            rwa_yields = fetcher.get_rwa_yields()
            defi_rates = fetcher.get_defi_rates()
            bera_pools = fetcher.get_bera_pools()
            
            # Step 2: Generate signals
            rwa_signals = rwa_arb.find_opportunities(rwa_yields, defi_rates)
            best_pool = lp_optimizer.optimize(bera_pools)
            
            # Step 3: Execute trades
            for signal in rwa_signals:
                executor.safe_execute(signal)
                
            if best_pool:
                # Example LP allocation signal
                lp_signal = TradeSignal(
                    asset=best_pool['pair'],
                    amount=0.2,  # 20% allocation
                    direction='ADD_LIQUIDITY'
                )
                executor.safe_execute(lp_signal)
                
            # Cooldown period
            time.sleep(60)  # 1 min between iterations
            
        except Exception as e:
            print(f"Critical error: {e}")
            time.sleep(300)  # Backoff on failure

if __name__ == "__main__":
    trading_loop()