# trade_simulator/ui/styles.py
from tkinter import ttk

def configure_styles():
    """Configure custom ttk styles for the application"""
    style = ttk.Style()
    style.theme_use("clam")
    
    # Configure frame styles
    style.configure("Custom.TFrame", background="#ffffff", borderwidth=2, relief="solid")
    style.configure("Header.TFrame", background="#2c3e50")
    
    # Configure label styles
    style.configure("Header.TLabel", background="#2c3e50", foreground="#ffffff", font=("Arial", 14, "bold"))
    style.configure("Title.TLabel", font=("Arial", 12, "bold"))
    style.configure("Output.TLabel", font=("Courier", 11))
    
    # Configure button styles
    style.configure("Start.TButton", background="#27ae60", foreground="#ffffff", font=("Arial", 10, "bold"))
    style.configure("Stop.TButton", background="#c0392b", foreground="#ffffff", font=("Arial", 10, "bold"))
    
    return style