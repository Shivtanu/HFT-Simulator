# models.py
from sklearn.linear_model import LinearRegression
import numpy as np

class SlippageModel:
    def __init__(self):
        # Dummy model for now — we'll train/update it live
        self.model = LinearRegression()
        # Fake training data (for testing)
        X = np.array([[100, 0.01, 0.2], [500, 0.02, -0.1], [1000, 0.03, 0.5]])
        y = np.array([0.1, 0.3, 0.8])  # slippage %
        self.model.fit(X, y)

    def predict(self, order_size, volatility, imbalance):
        features = np.array([[order_size, volatility, imbalance]])
        return self.model.predict(features)[0]

class MarketImpactModel:
    def __init__(self, gamma=1e-6, risk_aversion=0.01):
        self.gamma = gamma  # Market impact coefficient
        self.lambda_ = risk_aversion

    def compute_impact_cost(self, X, sigma, T):
        """
        Estimate market impact cost using Almgren-Chriss model.
        X: Order size (USD)
        sigma: Volatility (as fraction, e.g., 0.01)
        T: Time window for execution in seconds
        """
        impact_cost = self.gamma * (X ** 2) / T
        risk_cost = self.lambda_ * (sigma ** 2) * (X ** 2) * T / 6
        return impact_cost + risk_cost
