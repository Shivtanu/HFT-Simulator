class TradeSimulator:
    def __init__(self, orderbook, fee_rate=0.001):
        self.orderbook = orderbook
        self.fee_rate = fee_rate

    def simulate_market_buy(self, usd_amount):
        cost = 0
        remaining = usd_amount
        for ask in self.orderbook.asks:
            price = float(ask[0])
            qty = float(ask[1])
            trade_value = price * qty
            if remaining <= trade_value:
                cost += remaining
                break
            else:
                cost += trade_value
                remaining -= trade_value
        fee = cost * self.fee_rate
        return cost, fee
