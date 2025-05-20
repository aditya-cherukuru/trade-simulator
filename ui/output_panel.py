# trade_simulator/ui/output_panel.py
import tkinter as tk
from tkinter import ttk
from ..utils.logger import setup_logger

class OutputPanel:
    """
    Class representing the output parameters panel of the application
    """
    def __init__(self, parent_frame):
        """
        Initialize the output panel
        
        Args:
            parent_frame: The parent frame where this panel will be placed
        """
        self.parent = parent_frame
        self.logger = setup_logger("OutputPanel")
        
        # Initialize variables
        self.slippage_var = tk.StringVar(value="0.00%")
        self.fees_var = tk.StringVar(value="$0.00")
        self.market_impact_var = tk.StringVar(value="$0.00")
        self.net_cost_var = tk.StringVar(value="$0.00")
        self.maker_taker_var = tk.StringVar(value="0%/100%")
        self.latency_var = tk.StringVar(value="0.00 ms")
        self.current_price_var = tk.StringVar(value="$0.00")
        self.status_var = tk.StringVar(value="Disconnected")
        
        # Set up UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface for the output panel"""
        # Output header
        output_header = ttk.Frame(self.parent, style="Header.TFrame")
        output_header.pack(fill=tk.X, padx=0, pady=0)
        ttk.Label(output_header, text="Output Parameters", 
                 style="Header.TLabel").pack(pady=10)
        
        # Output parameters frame
        output_params_frame = ttk.Frame(self.parent)
        output_params_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Expected Slippage
        ttk.Label(output_params_frame, text="Expected Slippage:", style="Title.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(output_params_frame, textvariable=self.slippage_var, style="Output.TLabel").grid(row=0, column=1, sticky=tk.E, padx=10, pady=5)
        
        # Expected Fees
        ttk.Label(output_params_frame, text="Expected Fees:", style="Title.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(output_params_frame, textvariable=self.fees_var, style="Output.TLabel").grid(row=1, column=1, sticky=tk.E, padx=10, pady=5)
        
        # Expected Market Impact
        ttk.Label(output_params_frame, text="Expected Market Impact:", style="Title.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(output_params_frame, textvariable=self.market_impact_var, style="Output.TLabel").grid(row=2, column=1, sticky=tk.E, padx=10, pady=5)
        
        # Net Cost
        ttk.Label(output_params_frame, text="Net Cost:", style="Title.TLabel").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Label(output_params_frame, textvariable=self.net_cost_var, style="Output.TLabel").grid(row=3, column=1, sticky=tk.E, padx=10, pady=5)
        
        # Maker/Taker proportion
        ttk.Label(output_params_frame, text="Maker/Taker proportion:", style="Title.TLabel").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Label(output_params_frame, textvariable=self.maker_taker_var, style="Output.TLabel").grid(row=4, column=1, sticky=tk.E, padx=10, pady=5)
        
        # Internal Latency
        ttk.Label(output_params_frame, text="Internal Latency:", style="Title.TLabel").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Label(output_params_frame, textvariable=self.latency_var, style="Output.TLabel").grid(row=5, column=1, sticky=tk.E, padx=10, pady=5)
        
        # Current Price
        ttk.Label(output_params_frame, text="Current Price:", style="Title.TLabel").grid(row=6, column=0, sticky=tk.W, pady=5)
        ttk.Label(output_params_frame, textvariable=self.current_price_var, style="Output.TLabel").grid(row=6, column=1, sticky=tk.E, padx=10, pady=5)
        
        # Status
        ttk.Label(output_params_frame, text="Connection Status:", style="Title.TLabel").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.status_label = ttk.Label(output_params_frame, textvariable=self.status_var, style="Output.TLabel")
        self.status_label.grid(row=7, column=1, sticky=tk.E, padx=10, pady=5)
        
        # Configure grid weights
        output_params_frame.columnconfigure(1, weight=1)
    
    def update_values(self, values):
        """
        Update the output values
        
        Args:
            values (dict): Dictionary with new values
        """
        try:
            if 'slippage' in values:
                self.slippage_var.set(f"{values['slippage']*100:.4f}%")
            if 'fees' in values:
                self.fees_var.set(f"${values['fees']:.4f}")
            if 'market_impact' in values:
                self.market_impact_var.set(f"${values['market_impact']:.4f}")
            if 'net_cost' in values:
                self.net_cost_var.set(f"${values['net_cost']:.4f}")
            if 'maker_proportion' in values:
                maker = values['maker_proportion']
                taker = 1 - maker
                self.maker_taker_var.set(f"{maker*100:.1f}%/{taker*100:.1f}%")
            if 'latency' in values:
                self.latency_var.set(f"{values['latency']*1000:.2f} ms")
            if 'price' in values:
                self.current_price_var.set(f"${values['price']:.2f}")
            if 'status' in values:
                self.status_var.set(values['status'])
        except Exception as e:
            self.logger.error(f"Error updating output values: {e}")
            
            
    def update_status(self, status):
        """
        Update the connection status display
        
        Args:
            status (str): Status message to display
        """
        try:
            self.status_var.set(status)
            # Change label color based on status
            if status == "Connected":
                self.status_label.configure(foreground="green")
            elif status == "Disconnected":
                self.status_label.configure(foreground="red")
            else:
                self.status_label.configure(foreground="orange")
        except Exception as e:
            self.logger.error(f"Error updating status: {e}")
    
    def update_price(self, price):
        """
        Update the current price display
        
        Args:
            price (float): Current price to display
        """
        try:
            self.current_price_var.set(f"${price:.2f}")
        except Exception as e:
            self.logger.error(f"Error updating price: {e}")

    def update_metrics(self, orderbook, params, mid_price, latency):
        """
        Update all output metrics
        
        Args:
            orderbook (dict): Current orderbook data
            params (dict): Input parameters
            mid_price (float): Current mid price
            latency (float): Current processing latency
        """
        try:
            from trade_simulator.models.trading_models import TradingModels
            
            models = TradingModels()
            
            # Calculate all metrics
            maker_proportion = models.predict_maker_taker(orderbook, params['quantity'])
            slippage = models.calculate_slippage(orderbook, params['quantity'], params['order_type'])
            fees = models.calculate_fees(params['exchange'], params['fee_tier'], 
                                    params['quantity'], mid_price, maker_proportion)
            market_impact = models.calculate_market_impact(orderbook, params['quantity'], 
                                                        params['volatility'], mid_price)
            
            # Calculate net cost
            net_cost = (params['quantity'] * mid_price) * (1 + slippage) + fees + market_impact
            
            # Update display values
            self.slippage_var.set(f"{slippage*100:.4f}%")
            self.fees_var.set(f"${fees:.2f}")
            self.market_impact_var.set(f"${market_impact:.2f}")
            self.net_cost_var.set(f"${net_cost:.2f}")
            self.maker_taker_var.set(f"{maker_proportion*100:.1f}%/{(1-maker_proportion)*100:.1f}%")
            self.latency_var.set(f"{latency*1000:.2f} ms")
            
        except Exception as e:
            self.logger.error(f"Error updating metrics: {e}")