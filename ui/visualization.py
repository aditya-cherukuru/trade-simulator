#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Trade Simulator - Orderbook Visualization Component
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging

logger = logging.getLogger("TradeSimulator")

class OrderbookVisualization:
    """
    Orderbook visualization component for the Trade Simulator
    """
    def __init__(self, parent):
        self.parent = parent
        self.setup_visualization()
    
    def setup_visualization(self):
        """Set up the visualization component"""
        # Create a header for the visualization
        viz_header = ttk.Frame(self.parent, style="Header.TFrame")
        viz_header.pack(fill=tk.X, padx=0, pady=(20, 0))
        ttk.Label(viz_header, text="Orderbook Visualization", 
                 style="Header.TLabel").pack(pady=10)
        
        # Create a frame for the visualization
        self.viz_frame = ttk.Frame(self.parent)
        self.viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(5, 3), dpi=80)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize empty plot
        self.initialize_plot()
    
    def initialize_plot(self):
        """Initialize the orderbook plot"""
        self.ax.set_title("Order Book Depth")
        self.ax.set_xlabel("Price")
        self.ax.set_ylabel("Quantity")
        
        # Initialize plot data
        self.bid_bars = self.ax.bar([], [], color='green', alpha=0.5, label='Bids')
        self.ask_bars = self.ax.bar([], [], color='red', alpha=0.5, label='Asks')
        self.ax.legend()
        
        self.canvas.draw()
    
    def update_visualization(self, orderbook):
        """Update the orderbook visualization with new data"""
        try:
            if not orderbook:
                return
                
            # Clear previous plot
            self.ax.clear()
            
            # Extract price and quantity for asks and bids
            ask_prices = [float(level[0]) for level in orderbook['asks'][:10]]
            ask_quantities = [float(level[1]) for level in orderbook['asks'][:10]]
            
            bid_prices = [float(level[0]) for level in orderbook['bids'][:10]]
            bid_quantities = [float(level[1]) for level in orderbook['bids'][:10]]
            
            # Create the plot
            self.ax.bar(ask_prices, ask_quantities, color='red', alpha=0.5, label='Asks')
            self.ax.bar(bid_prices, bid_quantities, color='green', alpha=0.5, label='Bids')
            
            # Set labels and title
            self.ax.set_title("Order Book Depth")
            self.ax.set_xlabel("Price")
            self.ax.set_ylabel("Quantity")
            self.ax.legend()
            
            # Format x-axis to show fewer price labels and with proper formatting
            self.ax.tick_params(axis='x', rotation=45)
            
            # Refresh canvas
            self.canvas.draw()
        except Exception as e:
            logger.error(f"Error updating orderbook visualization: {e}")