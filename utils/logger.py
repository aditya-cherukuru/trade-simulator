# trade_simulator/utils/logger.py
import logging

def setup_logger(name="TradeSimulator"):
    """Configure and return a logger with the specified name"""
    logger = logging.getLogger(name)
    
    # Only set up handlers if they don't exist to prevent duplicate logs
    if not logger.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("trade_simulator.log"),
                logging.StreamHandler()
            ]
        )
    
    return logger