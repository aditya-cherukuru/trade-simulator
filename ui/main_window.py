#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Trade Simulator - Main Window UI Component
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from trade_simulator.ui.input_panel import InputPanel
from trade_simulator.ui.output_panel import OutputPanel
from trade_simulator.ui.visualization import OrderbookVisualization
from trade_simulator.ui.styles import configure_styles
from trade_simulator.network.websocket_client import WebSocketClient

# Remove duplicate import
# from .input_panel import InputPanel

logger = logging.getLogger("TradeSimulator")

# ...rest of the file remains the same...

class TradeSimulatorWindow:
    """
    Main application window for the Trade Simulator
    """
    def __init__(self, root):
        self.root = root
        self.root.title("GoQuant Trade Simulator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize data structures
        self.websocket_client = None
        self.orderbook = None
        
        # Configure styles
        configure_styles()
        
        # Create UI components
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Create header
        self.create_header()
        
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left panel (inputs)
        left_frame = ttk.Frame(main_container, style="Custom.TFrame")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create right panel (outputs)
        right_frame = ttk.Frame(main_container, style="Custom.TFrame")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create input panel
        self.input_panel = InputPanel(left_frame)
        
        # Create visualization panel
        self.visualization = OrderbookVisualization(left_frame)
        
        # Create output panel
        self.output_panel = OutputPanel(right_frame)
        
        # Create control buttons
        self.create_control_buttons()
    
    def create_header(self):
        """Create the header frame"""
        header_frame = ttk.Frame(self.root, style="Header.TFrame")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # App title
        ttk.Label(header_frame, text="GoQuant Trade Simulator", 
                 style="Header.TLabel").pack(pady=10)
    
    def create_control_buttons(self):
        """Create control buttons"""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Start button
        self.start_button = ttk.Button(button_frame, text="Start Simulation", 
                                      command=self.start_simulation, style="Start.TButton")
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # Stop button
        self.stop_button = ttk.Button(button_frame, text="Stop Simulation", 
                                     command=self.stop_simulation, style="Stop.TButton")
        self.stop_button.pack(side=tk.LEFT, padx=10)
        self.stop_button.configure(state=tk.DISABLED)
    
    def start_simulation(self):
        """Start the trade simulation"""
        try:
            # Update UI state
            self.start_button.configure(state=tk.DISABLED)
            self.stop_button.configure(state=tk.NORMAL)
            self.output_panel.update_status("Connecting...")
            
            # Get parameters from input panel
            asset = self.input_panel.get_spot_asset()
            
            # Create WebSocket URI
            uri = f"wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/{asset}"
            
            # Initialize WebSocket client
            self.websocket_client = WebSocketClient(uri, self.process_orderbook_data)
            self.websocket_client.start()
            
            # Start update loop
            self.update_loop()
            
            logger.info(f"Simulation started for {asset}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start simulation: {e}")
            logger.error(f"Failed to start simulation: {e}")
            self.stop_simulation()
    
    def stop_simulation(self):
        """Stop the trade simulation"""
        try:
            # Stop WebSocket client
            if self.websocket_client:
                self.websocket_client.stop()
                self.websocket_client = None
            
            # Update UI state
            self.start_button.configure(state=tk.NORMAL)
            self.stop_button.configure(state=tk.DISABLED)
            self.output_panel.update_status("Disconnected")
            
            logger.info("Simulation stopped")
        except Exception as e:
            logger.error(f"Error stopping simulation: {e}")
    
    def process_orderbook_data(self, data):
        """Process orderbook data received from WebSocket"""
        try:
            self.orderbook = data
            
            # Update status
            self.output_panel.update_status("Connected")
        except Exception as e:
            logger.error(f"Error processing orderbook data: {e}")
    
    def update_loop(self):
        """Update UI with latest calculations"""
        if not self.websocket_client or not self.websocket_client.running:
            return
        
        try:
            # Check if we've received orderbook data
            if self.orderbook:
                # Get input values from input panel
                params = self.input_panel.get_all_parameters()
                
                # Calculate mid price
                mid_price = (float(self.orderbook['asks'][0][0]) + float(self.orderbook['bids'][0][0])) / 2
                
                # Update current price in output panel
                self.output_panel.update_price(mid_price)
                
                # Update output panel with calculated metrics
                self.output_panel.update_metrics(
                    self.orderbook, 
                    params, 
                    mid_price,
                    self.websocket_client.average_processing_time
                )
                
                # Update visualization
                self.visualization.update_visualization(self.orderbook)
            
            # Schedule next update
            self.root.after(100, self.update_loop)
        except Exception as e:
            logger.error(f"Error in update loop: {e}")
            self.root.after(100, self.update_loop)