from pydantic import BaseModel
from enum import Enum
from typing import Optional

class TradeSignal(BaseModel):
    asset: str
    amount: float
    direction: str  # BUY/SELL
    chain: str = 'berachain'

class Chain(Enum):
    BERACHAIN = "berachain"
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    BSC = "bsc"

class PoolData(BaseModel):
    chain: Chain
    pair: str
    tvl: float
    apr: float
    il_risk: float
    volume_24h: float
    fee_apr: Optional[float] = None
    reward_apr: Optional[float] = None
    timestamp: Optional[int] = None

class LiquidityAction(Enum):
    ADD_LIQUIDITY = "ADD_LIQUIDITY"
    REMOVE_LIQUIDITY = "REMOVE_LIQUIDITY"

class LiquiditySignal(BaseModel):
    chain: Chain
    pair: str
    action: LiquidityAction
    amount: float

class MarketConditions(BaseModel):
    trading_halted: bool
    position_cap: float