# trade_simulator/models/trading_models.py
import numpy as np
import logging
from ..utils.logger import setup_logger

class TradingModels:
    """
    Class containing all trading models for cost estimation
    """
    def __init__(self):
        """Initialize the TradingModels class"""
        self.logger = setup_logger("TradingModels")
    
    def calculate_slippage(self, orderbook, quantity, order_type="market"):
        """
        Calculate expected slippage using linear regression
        """
        if order_type != "market":
            return 0.0
        
        # For market orders, calculate slippage based on depth available
        try:
            if not orderbook or not orderbook.get('asks') or not orderbook.get('bids'):
                return 0.0
                
            # Get mid price
            best_ask = float(orderbook['asks'][0][0])
            best_bid = float(orderbook['bids'][0][0])
            mid_price = (best_ask + best_bid) / 2
            
            # For buy orders, we walk up the ask book
            total_filled = 0
            total_cost = 0
            
            for price_level, size in orderbook['asks']:
                price = float(price_level)
                available = float(size)
                
                if total_filled + available >= quantity:
                    # This level will complete our order
                    remaining = quantity - total_filled
                    total_cost += remaining * price
                    total_filled = quantity
                    break
                else:
                    # Take all available at this level and continue
                    total_cost += available * price
                    total_filled += available
                    
            if total_filled < quantity:
                # Not enough depth in the orderbook for the specified quantity
                return 0.02  # Return a default 2% slippage
                
            # Calculate effective price
            effective_price = total_cost / quantity
            
            # Slippage is the percentage difference from mid price
            slippage = (effective_price - mid_price) / mid_price
            
            return max(0, slippage)  # Ensure slippage is non-negative
        except Exception as e:
            self.logger.error(f"Error calculating slippage: {e}")
            return 0.01  # Default slippage value
    
    def calculate_fees(self, exchange, fee_tier, quantity, price, maker_taker_proportion):
        """
        Calculate exchange fees based on exchange fee tier and maker/taker proportion
        """
        try:
            # Fee rates from OKX documentation (for example)
            fee_rates = {
                "VIP0": {"maker": 0.0008, "taker": 0.001},
                "VIP1": {"maker": 0.0007, "taker": 0.0009},
                "VIP2": {"maker": 0.0006, "taker": 0.0008},
                "VIP3": {"maker": 0.0005, "taker": 0.0007},
                "VIP4": {"maker": 0.0003, "taker": 0.0005},
                "VIP5": {"maker": 0.0000, "taker": 0.0003},
            }
            
            if exchange.lower() != "okx" or fee_tier not in fee_rates:
                # Default to VIP0 if not specified or invalid
                maker_fee = 0.0008
                taker_fee = 0.001
            else:
                maker_fee = fee_rates[fee_tier]["maker"]
                taker_fee = fee_rates[fee_tier]["taker"]
            
            # Calculate weighted fee based on maker/taker proportion
            maker_portion = maker_taker_proportion
            taker_portion = 1 - maker_portion
            
            weighted_fee_rate = (maker_fee * maker_portion) + (taker_fee * taker_portion)
            fee_amount = quantity * price * weighted_fee_rate
            
            return fee_amount
        except Exception as e:
            self.logger.error(f"Error calculating fees: {e}")
            return quantity * price * 0.001  # Default to 0.1% fee
    
    def calculate_market_impact(self, orderbook, quantity, volatility, price):
        """
        Implementation of Almgren-Chriss market impact model
        Market impact = σ * √τ * (quantity/V) * price
        where:
        - σ is volatility
        - τ is time horizon (normalize to 1 day)
        - V is daily volume
        - quantity is order size
        """
        try:
            # Estimate market depth as sum of available liquidity in top N levels
            depth = 0
            for i in range(min(10, len(orderbook['bids']))):
                depth += float(orderbook['bids'][i][1])
            for i in range(min(10, len(orderbook['asks']))):
                depth += float(orderbook['asks'][i][1])
            
            # If depth is too small, use a reasonable default
            if depth < quantity:
                depth = quantity * 100
            
            # Almgren-Chriss parameters
            sigma = volatility  # Volatility parameter
            tau = 1/24  # Assuming ~1 hour execution time (fraction of day)
            
            # Temporary impact factor (based on market depth)
            temporary_impact = sigma * np.sqrt(tau) * (quantity / depth) * price
            
            # Permanent impact (usually smaller)
            permanent_impact = temporary_impact * 0.3
            
            # Total market impact
            total_impact = temporary_impact + permanent_impact
            
            return total_impact
        except Exception as e:
            self.logger.error(f"Error calculating market impact: {e}")
            return quantity * price * 0.005  # Default to 0.5% market impact
    
    def predict_maker_taker(self, orderbook, quantity):
        """
        Use logistic regression to predict maker/taker proportion
        Returns proportion that will be maker orders (0-1)
        """
        try:
            if not orderbook or not orderbook.get('asks') or not orderbook.get('bids'):
                return 0.0  # Default to all taker orders
                
            # Calculate spread
            best_ask = float(orderbook['asks'][0][0])
            best_bid = float(orderbook['bids'][0][0])
            spread = (best_ask - best_bid) / best_bid
            
            # Calculate order book imbalance (more bids than asks suggests higher liquidity on buy side)
            bid_volume = sum(float(level[1]) for level in orderbook['bids'][:5])
            ask_volume = sum(float(level[1]) for level in orderbook['asks'][:5])
            
            if bid_volume + ask_volume == 0:
                imbalance = 0
            else:
                imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume)
            
            # Simple logistic function to determine maker proportion
            # Tighter spreads and higher liquidity on ask side make maker orders more likely
            maker_proportion = 1 / (1 + np.exp(5 * (spread - 0.001) - imbalance))
            
            # Constrain between 0 and 0.8 (assuming some portion will always be taker)
            return max(0, min(0.8, maker_proportion))
        except Exception as e:
            self.logger.error(f"Error predicting maker/taker proportion: {e}")
            return 0.2  # Default maker proportion