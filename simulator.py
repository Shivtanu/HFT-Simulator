from models import SlippageModel, MarketImpactModel

class TradeSimulator:
    def __init__(self, orderbook):
        self.orderbook = orderbook
        self.slippage_model = SlippageModel()
        self.impact_model = MarketImpactModel()
        self.fee_rate = 0.001  # 0.1%

    def simulate_market_buy(self, quantity_usd, volatility=0.01, T=10):
        if not self.orderbook.asks:
            return 0, 0, 0, 0

        total_cost = 0
        remaining = quantity_usd
        for price, qty in self.orderbook.asks:
            trade_qty = min(qty * price, remaining)
            total_cost += trade_qty
            remaining -= trade_qty
            if remaining <= 0:
                break

        fee = total_cost * self.fee_rate

        # Calculate imbalance
        bid_volume = sum(qty for _, qty in self.orderbook.bids[:3])
        ask_volume = sum(qty for _, qty in self.orderbook.asks[:3])
        imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume + 1e-9)

        # Slippage
        slippage_pct = self.slippage_model.predict(quantity_usd, volatility, imbalance)
        slippage_cost = total_cost * slippage_pct

        # Market Impact
        impact_cost = self.impact_model.compute_impact_cost(quantity_usd, volatility, T)

        # Net Cost
        net_cost = total_cost + fee + slippage_cost + impact_cost

        return net_cost, fee, slippage_cost, impact_cost
