export interface SwapPayload {
    action: 'buy' | 'sell';
    asset: string;
    amount: number;
  }