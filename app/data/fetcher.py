# app/data/fetcher.py
import requests
import os
from enum import Enum
from typing import List, Dict, Optional
import time
from cachetools import TTLCache, cached
from cachetools.keys import hashkey
from pydantic import BaseModel
import numpy as np

class Chain(Enum):
    BERACHAIN = "berachain"
    ETHEREUM = "ethereum"
    BSC = "bsc"
    POLYGON = "polygon"

class PoolData(BaseModel):
    pair: str
    tvl: float
    apr: float
    il_risk: float
    volume_24h: float
    fee_apr: Optional[float] = None
    reward_apr: Optional[float] = None
    timestamp: Optional[int] = None

class RWADataFetcher:
    def __init__(self):
        self.rwa_endpoint = os.getenv('RWA_API', 'https://api.ondo.finance/v1')
        self.cache = TTLCache(maxsize=100, ttl=300)  # Cache for 5 minutes

    @cached(cache=TTLCache(maxsize=10, ttl=600))
    def get_rwa_yields(self) -> Dict[str, float]:
        """Fetch RWA yields from Ondo/Centrifuge APIs."""
        try:
            res = requests.get(f"{self.rwa_endpoint}/yields", timeout=5)
            res.raise_for_status()
            return {item['asset']: item['apy'] for item in res.json()['data']}
        except Exception as e:
            print(f"RWA API Error: {e}")
            return {'OUSG': 0.051, 'STBT': 0.049}  # Fallback values

    @cached(cache=TTLCache(maxsize=10, ttl=600))
    def get_rwa_prices(self) -> Dict[str, float]:
        """Fetch RWA token prices from Ondo API."""
        try:
            res = requests.get(f"{self.rwa_endpoint}/prices", timeout=5)
            res.raise_for_status()
            return {item['asset']: item['price'] for item in res.json()['data']}
        except Exception as e:
            print(f"RWA API Error: {e}")
            return {'OUSG': 1.02, 'STBT': 1.01}  # Fallback values

    def get_rwa_arbitrage_opportunities(self, defi_rates: Dict[str, float]) -> Dict[str, Dict]:
        """
        Identify RWA arbitrage opportunities by comparing yields vs DeFi rates.
        """
        rwa_yields = self.get_rwa_yields()
        opportunities = {}
        for asset, rwa_yield in rwa_yields.items():
            spread = rwa_yield - defi_rates.get('USDC', 0.045)  # Compare vs USDC
            if spread > 0.015:  # 1.5% minimum arbitrage
                opportunities[asset] = {
                    'action': 'BUY_RWA',
                    'spread': spread,
                    'yield': rwa_yield
                }
        return opportunities

class DexDataFetcher:
    DEX_PROTOCOLS = {
        Chain.BERACHAIN: 'bex',
        Chain.ETHEREUM: 'uniswap-v3',
        Chain.BSC: 'pancakeswap-v3',
        Chain.POLYGON: 'quickswap-v3'
    }

    def __init__(self):
        self.base_url = "https://api.llama.fi"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'DeFi-Kaiser/1.0'})
        
    @cached(TTLCache(maxsize=100, ttl=300), key=lambda self, chain: hashkey(chain.value))
    def get_dex_pools(self, chain: Chain) -> List[PoolData]:
        """Get comprehensive pool data with enhanced caching"""
        try:
            pools = self._get_pools_data(chain)
            yields = self._get_yields_data(chain)
            return self._process_pool_data(pools, yields)
        except Exception as e:
            print(f"Failed to fetch DEX data: {e}")
            return self._get_fallback_data(chain)

    def _get_pools_data(self, chain: Chain) -> List[Dict]:
        """Fetch enriched pool data with volume and TVL"""
        url = f"{self.base_url}/pools/v2"
        params = {
            'chain': chain.value,
            'protocol': self.DEX_PROTOCOLS[chain]
        }
        res = self.session.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()['data']

    def _get_yields_data(self, chain: Chain) -> Dict[str, float]:
        """Fetch APR data with detailed breakdown"""
        url = f"{self.base_url}/yields"
        params = {
            'chain': chain.value,
            'protocol': self.DEX_PROTOCOLS[chain]
        }
        res = self.session.get(url, params=params, timeout=10)
        res.raise_for_status()
        return {item['pool']: item for item in res.json()}

    def _calculate_il_risk(self, pool: Dict) -> float:
        """Enhanced IL risk calculation using multiple factors"""
        try:
            # Volatility from 7d price changes
            price_change = abs(pool.get('priceChange7d', 0)) / 100
            volume_tvl_ratio = pool.get('volume24h', 0) / max(pool.get('tvlUsd', 1), 1)
            
            # Combine factors using weighted average
            return min(
                0.5 * price_change + 
                0.3 * (1 - np.tanh(volume_tvl_ratio)) + 
                0.2 * (1 - pool.get('feeTier', 0.3)/10000),
                1.0
            )
        except Exception as e:
            print(f"IL calculation error: {e}")
            return 0.15

    def _process_pool_data(self, pools: List[Dict], yields: Dict) -> List[PoolData]:
        """Process and merge data from multiple endpoints"""
        processed = []
        for pool in pools:
            try:
                yield_data = yields.get(pool['pool'], {})
                processed.append(PoolData(
                    pair=pool['symbol'],
                    tvl=pool['tvlUsd'],
                    apr=yield_data.get('apy', 0),
                    il_risk=self._calculate_il_risk(pool),
                    volume_24h=pool['volume24h'],
                    fee_apr=yield_data.get('feeApy', 0),
                    reward_apr=yield_data.get('rewardApy', 0),
                    timestamp=int(time.time())
                ))
            except KeyError as e:
                print(f"Missing key {e} in pool data")
        return processed

    def _get_fallback_data(self, chain: Chain) -> List[PoolData]:
        """Improved fallback data with chain-specific defaults"""
        return [
            PoolData(
                pair='BERA/USDC' if chain == Chain.BERACHAIN else 'ETH/USDC',
                tvl=1e6,
                apr=0.15,
                il_risk=0.1,
                volume_24h=500000,
                fee_apr=0.05,
                reward_apr=0.05,
                timestamp=int(time.time())
            )
        ]