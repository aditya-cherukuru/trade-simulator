import unittest
import numpy as np
from models.trading_models import TradingModels

class TestTradingModels(unittest.TestCase):
    def setUp(self):
        self.model = TradingModels()
        self.sample_orderbook = {
            "asks": [["100.0", "1.0"], ["101.0", "2.0"]],
            "bids": [["99.0", "1.0"], ["98.0", "2.0"]]
        }

    def test_slippage_calculation(self):
        slippage = self.model.calculate_slippage(self.sample_orderbook, 1.0)
        self.assertGreaterEqual(slippage, 0)
        self.assertLessEqual(slippage, 0.1)

    def test_market_impact(self):
        impact = self.model.calculate_market_impact(
            self.sample_orderbook, 
            quantity=1.0,
            volatility=0.02,
            price=100.0
        )
        self.assertGreaterEqual(impact, 0)

    def test_maker_taker_prediction(self):
        ratio = self.model.predict_maker_taker(self.sample_orderbook, 1.0)
        self.assertGreaterEqual(ratio, 0)
        self.assertLessEqual(ratio, 1)

    def test_fee_calculation(self):
        fees = self.model.calculate_fees(
            exchange="OKX",
            fee_tier="VIP0",
            quantity=1.0,
            price=100.0,
            maker_taker_proportion=0.6
        )
        self.assertGreaterEqual(fees, 0)

if __name__ == '__main__':
    unittest.main()