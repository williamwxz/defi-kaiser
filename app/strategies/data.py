from pydantic import BaseModel

class TradeSignal(BaseModel):
    asset: str
    amount: float
    direction: str  # BUY/SELL
    chain: str = 'berachain'