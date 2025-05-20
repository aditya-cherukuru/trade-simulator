#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Trade Simulator - Main entry point
"""

import sys
import os
import tkinter as tk
from tkinter import ttk

import logging
from trade_simulator.ui.main_window import TradeSimulatorWindow
from trade_simulator.utils.logger import setup_logger


def main():
    """Main function to start the application"""
    try:
        # Setup logging
        setup_logger()
        logger = logging.getLogger("TradeSimulator")
        logger.info("Starting Trade Simulator application")
        
        # Create and start the main application window
        root = tk.Tk()
        app = TradeSimulatorWindow(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Application error: {e}")


if __name__ == "__main__":
    main()