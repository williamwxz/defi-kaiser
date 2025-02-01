# app/data.py
import requests
from web3 import Web3
import os

class DataFetcher:
    def __init__(self):
        self.rwa_endpoint = os.getenv('RWA_API', 'https://api.ondo.finance/v1/yields')
        self.bera_node = os.getenv('BERA_RPC', 'https://rpc.berachain.com')
        self.w3 = Web3(Web3.HTTPProvider(self.bera_node))

    def get_rwa_yields(self):
        """Fetch tokenized RWA yields from Ondo/Centrifuge"""
        try:
            res = requests.get(self.rwa_endpoint, timeout=3)
            return {item['asset']: item['apy'] for item in res.json()['data']}
        except Exception as e:
            print(f"RWA API Error: {e}")
            return {'OUSG': 0.051, 'STBT': 0.049}  # Fallback values

    def get_bera_pools(self):
        """Get Berachain DEX pool data (simplified)"""
        # In production: Use Berachain SDK or Subgraph
        return [
            {'pair': 'BERA/USDC', 'apr': 0.45, 'tvl': 1.2e6},
            {'pair': 'BGT/USDC', 'apr': 0.68, 'tvl': 850e3}
        ]

    def get_defi_rates(self):
        """Get DeFi lending rates from major protocols"""
        # Simulated data - integrate with Aave/Compound APIs
        return {'USDC': 0.048, 'USDT': 0.047, 'DAI': 0.049}