# trade_simulator/ui/input_panel.py
"""
Trade Simulator - Input Panel Component
"""
import tkinter as tk
from tkinter import ttk
from trade_simulator.utils.logger import setup_logger

class InputPanel:
    """
    Class representing the input parameters panel of the application
    """
    def __init__(self, parent_frame):
        """
        Initialize the input panel
        
        Args:
            parent_frame: The parent frame where this panel will be placed
        """
        self.parent = parent_frame
        self.logger = setup_logger("InputPanel")
        
        # Initialize variables
        self.exchange_var = tk.StringVar(value="OKX")
        self.spot_asset_var = tk.StringVar(value="BTC-USDT")
        self.order_type_var = tk.StringVar(value="market")
        self.quantity_var = tk.DoubleVar(value=100.0)
        self.volatility_var = tk.DoubleVar(value=2.0)
        self.fee_tier_var = tk.StringVar(value="VIP0")
        
        # Set up UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface for the input panel"""
        # Input header
        input_header = ttk.Frame(self.parent, style="Header.TFrame")
        input_header.pack(fill=tk.X, padx=0, pady=0)
        ttk.Label(input_header, text="Input Parameters", 
                 style="Header.TLabel").pack(pady=10)
        
        # Input parameters frame
        input_params_frame = ttk.Frame(self.parent)
        input_params_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Exchange
        ttk.Label(input_params_frame, text="Exchange:", style="Title.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5)
        exchange_entry = ttk.Entry(input_params_frame, textvariable=self.exchange_var, state="readonly")
        exchange_entry.grid(row=0, column=1, sticky=tk.EW, padx=10, pady=5)
        
        # Spot Asset
        ttk.Label(input_params_frame, text="Spot Asset:", style="Title.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        spot_asset_combo = ttk.Combobox(input_params_frame, textvariable=self.spot_asset_var)
        spot_asset_combo['values'] = ('BTC-USDT', 'ETH-USDT', 'SOL-USDT', 'XRP-USDT')
        spot_asset_combo.grid(row=1, column=1, sticky=tk.EW, padx=10, pady=5)
        
        # Order Type
        ttk.Label(input_params_frame, text="Order Type:", style="Title.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5)
        order_type_combo = ttk.Combobox(input_params_frame, textvariable=self.order_type_var)
        order_type_combo['values'] = ('market', 'limit', 'stop')
        order_type_combo.grid(row=2, column=1, sticky=tk.EW, padx=10, pady=5)
        
        # Quantity
        ttk.Label(input_params_frame, text="Quantity (USD):", style="Title.TLabel").grid(row=3, column=0, sticky=tk.W, pady=5)
        quantity_entry = ttk.Entry(input_params_frame, textvariable=self.quantity_var)
        quantity_entry.grid(row=3, column=1, sticky=tk.EW, padx=10, pady=5)
        
        # Volatility
        ttk.Label(input_params_frame, text="Volatility (%):", style="Title.TLabel").grid(row=4, column=0, sticky=tk.W, pady=5)
        volatility_entry = ttk.Entry(input_params_frame, textvariable=self.volatility_var)
        volatility_entry.grid(row=4, column=1, sticky=tk.EW, padx=10, pady=5)
        
        # Fee Tier
        ttk.Label(input_params_frame, text="Fee Tier:", style="Title.TLabel").grid(row=5, column=0, sticky=tk.W, pady=5)
        fee_tier_combo = ttk.Combobox(input_params_frame, textvariable=self.fee_tier_var)
        fee_tier_combo['values'] = ('VIP0', 'VIP1', 'VIP2', 'VIP3', 'VIP4', 'VIP5')
        fee_tier_combo.grid(row=5, column=1, sticky=tk.EW, padx=10, pady=5)
        
        # Configure grid weights
        input_params_frame.columnconfigure(1, weight=1)
    
    def get_values(self):
        """
        Get all input values
        
        Returns:
            dict: A dictionary containing all input values
        """
        return {
            "exchange": self.exchange_var.get(),
            "spot_asset": self.spot_asset_var.get(),
            "order_type": self.order_type_var.get(),
            "quantity": self.quantity_var.get(),
            "volatility": self.volatility_var.get() / 100.0,  # Convert to decimal
            "fee_tier": self.fee_tier_var.get()
        }
        
    
    def get_spot_asset(self):
        """
        Get the selected spot asset value
        
        Returns:
            str: The currently selected spot asset pair (e.g., 'BTC-USDT')
        """
        return self.spot_asset_var.get()
    
    
    def get_all_parameters(self):
        """
        Get all input parameters in a structured format
        
        Returns:
            dict: Dictionary containing all input parameters
        """
        return {
            "exchange": self.exchange_var.get(),
            "spot_asset": self.spot_asset_var.get(),
            "order_type": self.order_type_var.get(),
            "quantity": self.quantity_var.get(),
            "volatility": self.volatility_var.get() / 100.0,  # Convert percentage to decimal
            "fee_tier": self.fee_tier_var.get()
        }