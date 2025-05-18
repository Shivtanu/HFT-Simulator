class OrderBook:
    def __init__(self):
        self.bids = []
        self.asks = []

    def update(self, data):
        self.bids = data['bids']
        self.asks = data['asks']
