# app/data.py
import requests
from web3 import Web3
import os
from enum import Enum
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time
from cachetools import TTLCache
from dataclasses import dataclass

class Chain(Enum):
    BERACHAIN = "berachain"
    ETHEREUM = "ethereum"
    BSC = "bsc"
    POLYGON = "polygon"

@dataclass
class PoolData:
    pair: str
    tvl: float
    apr: float
    il_risk: float
    volume_24h: float
    fee_apr: Optional[float] = None
    reward_apr: Optional[float] = None
    timestamp: Optional[int] = None

class DataFetcher:
    def __init__(self):
        self.rwa_endpoint = os.getenv('RWA_API', 'https://api.ondo.finance/v1')
        self.bera_node = os.getenv('BERA_RPC', 'https://rpc.berachain.com')
        self.w3 = Web3(Web3.HTTPProvider(self.bera_node))

    def get_rwa_yields(self):
        """Fetch tokenized RWA yields from Ondo/Centrifuge"""
        try:
            res = requests.get(f"{self.rwa_endpoint}/yields", timeout=3)
            return {item['asset']: item['apy'] for item in res.json()['data']}
        except Exception as e:
            print(f"RWA API Error: {e}")
            return {'OUSG': 0.051, 'STBT': 0.049}  # Fallback values

    def get_dex_pools(self, chain: Chain):
        """Get Berachain DEX pool data (simplified)"""
        # In production: Use Berachain SDK or Subgraph
        return [
            {'pair': 'BERA/USDC', 'apr': 0.45, 'tvl': 1.2e6, 'il_risk': 0.1},
            {'pair': 'BGT/USDC', 'apr': 0.68, 'tvl': 850e3, 'il_risk': 0.15}
        ]

    def get_defi_rates(self):
        """Get DeFi lending rates from major protocols"""
        # Simulated data - integrate with Aave/Compound APIs
        return {'USDC': 0.048, 'USDT': 0.047, 'DAI': 0.049}
    
    def get_rwa_prices(self):
        """Fetch RWA token prices from Ondo API."""
        try:
            res = requests.get(f"{self.rwa_endpoint}/prices", timeout=3)
            return {item['asset']: item['price'] for item in res.json()['data']}
        except Exception as e:
            print(f"RWA API Error: {e}")
            return {'OUSG': 1.02, 'STBT': 1.01}

class DexDataFetcher:
    # Cache pool data for 5 minutes
    _pool_cache = TTLCache(maxsize=100, ttl=300)
    
    # Map your DEXes to DefiLlama protocol slugs
    DEX_PROTOCOLS = {
        Chain.BERACHAIN: 'bex',  # Replace with actual DefiLlama slug
        Chain.ETHEREUM: 'uniswap-v3',
        Chain.BSC: 'pancakeswap-v3',
        Chain.POLYGON: 'quickswap-v3'
    }

    def __init__(self):
        self.base_url = "https://api.llama.fi"
        self.session = requests.Session()
        # Add reasonable timeout
        self.session.request = lambda method, url, **kwargs: \
            requests.Session.request(self.session, method, url, timeout=10, **kwargs)

    def get_dex_pools(self, chain: Chain) -> List[PoolData]:
        """Get comprehensive pool data from DefiLlama"""
        cache_key = f"pools_{chain.value}"
        
        # Check cache first
        if cache_key in self._pool_cache:
            return self._pool_cache[cache_key]

        try:
            # Get protocol overview
            protocol_data = self._get_protocol_data(chain)
            
            # Get pool-specific data
            pools_data = self._get_pools_data(chain)
            
            # Get protocol yields
            yields_data = self._get_yields_data(chain)

            # Combine and process the data
            processed_pools = self._process_pool_data(
                pools_data, 
                yields_data, 
                protocol_data
            )

            # Cache the results
            self._pool_cache[cache_key] = processed_pools
            return processed_pools

        except Exception as e:
            print(f"Error fetching DefiLlama data for {chain}: {e}")
            return self._get_fallback_data(chain)

    def _get_protocol_data(self, chain: Chain) -> Dict:
        """Fetch protocol overview data"""
        protocol_slug = self.DEX_PROTOCOLS[chain]
        url = f"{self.base_url}/protocol/{protocol_slug}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def _get_pools_data(self, chain: Chain) -> List[Dict]:
        """Fetch pool-specific data"""
        protocol_slug = self.DEX_PROTOCOLS[chain]
        url = f"{self.base_url}/pools/v2"
        params = {
            'chain': chain.value,
            'protocol': protocol_slug
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()['data']

    def _get_yields_data(self, chain: Chain) -> List[Dict]:
        """Fetch yield/APR data"""
        protocol_slug = self.DEX_PROTOCOLS[chain]
        url = f"{self.base_url}/yields"
        params = {
            'chain': chain.value,
            'protocol': protocol_slug
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _calculate_il_risk(self, pool_data: Dict) -> float:
        """Calculate IL risk based on volatility and volume"""
        try:
            # Get volatility if available
            volatility = pool_data.get('volatility7d', None)
            
            if volatility is None:
                # Fallback: estimate from price change
                price_change = abs(pool_data.get('priceChange7d', 0))
                volatility = price_change / 100
            
            # Consider volume/TVL ratio in risk calculation
            volume = float(pool_data.get('volume24h', 0))
            tvl = float(pool_data.get('tvl', 1))  # avoid division by zero
            volume_tvl_ratio = volume / tvl if tvl > 0 else 0
            
            # Higher volume/TVL ratio typically means lower IL risk
            # as it indicates better liquidity and price stability
            il_risk = (volatility * 0.7) - (min(volume_tvl_ratio, 1) * 0.3)
            
            # Bound the risk between 0 and 1
            return max(min(il_risk, 1.0), 0.0)

        except Exception as e:
            print(f"Error calculating IL risk: {e}")
            return 0.1  # Default risk value

    def _process_pool_data(
        self, 
        pools_data: List[Dict], 
        yields_data: List[Dict], 
        protocol_data: Dict
    ) -> List[PoolData]:
        """Process and combine data from different endpoints"""
        processed_pools = []

        for pool in pools_data:
            try:
                # Find matching yield data
                yield_info = next(
                    (y for y in yields_data if y.get('pool') == pool.get('pool')),
                    {}
                )

                pool_data = PoolData(
                    pair=pool.get('symbol', ''),
                    tvl=float(pool.get('tvlUsd', 0)),
                    apr=float(yield_info.get('apy', 0)),
                    il_risk=self._calculate_il_risk(pool),
                    volume_24h=float(pool.get('volume24h', 0)),
                    fee_apr=float(yield_info.get('feeApy', 0)),
                    reward_apr=float(yield_info.get('rewardApy', 0)),
                    timestamp=int(time.time())
                )
                processed_pools.append(pool_data)

            except Exception as e:
                print(f"Error processing pool {pool.get('symbol', 'unknown')}: {e}")
                continue

        return processed_pools

    def _get_fallback_data(self, chain: Chain) -> List[PoolData]:
        """Return fallback data when API calls fail"""
        return [
            PoolData(
                pair='TOKEN1/TOKEN2',
                tvl=1000000,
                apr=0.1,
                il_risk=0.1,
                volume_24h=100000,
                fee_apr=0.05,
                reward_apr=0.05,
                timestamp=int(time.time())
            )
        ]

    def get_historical_tvl(self, chain: Chain, days: int = 30) -> List[Dict]:
        """Get historical TVL data"""
        protocol_slug = self.DEX_PROTOCOLS[chain]
        url = f"{self.base_url}/protocol/{protocol_slug}/historical"
        params = {'days': days}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching historical TVL: {e}")
            return [] 