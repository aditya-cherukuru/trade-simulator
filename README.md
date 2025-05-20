# GoQuant Trade Simulator

A high-performance trade simulator leveraging real-time market data to estimate transaction costs and market impact for cryptocurrency trading.

## Overview

This Trade Simulator connects to WebSocket endpoints that stream full L2 orderbook data from cryptocurrency exchanges. It processes this data in real-time to calculate various trading metrics including slippage, fees, market impact, and overall transaction costs.

## Features

- **Real-time data processing**: Connects to WebSocket endpoints for live L2 orderbook data
- **Cost estimation models**: Implements Almgren-Chriss market impact model, slippage estimation via regression, and fee calculation
- **Interactive visualization**: Displays orderbook depth in real-time
- **Performance metrics**: Measures and displays processing latency

## System Requirements

- Python 3.8+
- Required packages:
  - tkinter
  - numpy
  - pandas
  - scipy
  - matplotlib
  - websockets
  - asyncio

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aditya-cherukuru/trade-simulator.git
cd goquant-trade-simulator
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python app.py
```

## Application Architecture

The application follows a modular architecture with clear separation of concerns:

```
trade_simulator/
├── __init__.py          # Makes the directory a package
├── app.py               # Main entry point
├── models/
│   ├── __init__.py
│   └── trading_models.py # Trading cost models implementation
├── ui/
│   ├── __init__.py
│   ├── main_window.py   # Main application window
│   ├── input_panel.py   # Input parameters panel
│   ├── output_panel.py  # Output parameters panel
│   ├── visualization.py # Orderbook visualization
│   └── styles.py        # UI styles
├── network/
│   ├── __init__.py
│   └── websocket_client.py # WebSocket client implementation
├── utils/
│   ├── __init__.py
│   ├── logger.py        # Logging utilities
│   └── performance_monitor.py  # Performance monitoring utilities
├── tests/
│   ├── __init__.py
│   └── test_trading_models.py  # Unit tests for trading models
└── README.md            # Project documentation
```


## Model Implementation Details

### Almgren-Chriss Market Impact Model

The Almgren-Chriss model is used to estimate the market impact of trading a given quantity of an asset. The model calculates both temporary and permanent impact components:

- Temporary impact represents the immediate price movement during execution
- Permanent impact represents the lasting effect on the market price

The model is implemented in `models/trading_models.py` and follows the formula:

Market impact = σ * √τ * (quantity/V) * price

Where:
- σ is the volatility
- τ is the time horizon (normalized to 1 day)
- V is the daily volume or market depth
- quantity is the order size

### Slippage Estimation

Slippage is estimated by simulating the execution of an order against the current orderbook. For market orders, the algorithm walks through available liquidity at each price level to determine the effective execution price.

### Maker/Taker Proportion Prediction

A logistic regression approach is used to predict the proportion of an order that will be executed as maker vs. taker orders. The prediction considers current spread and orderbook imbalance as key features.

## Performance Optimization

The application implements several optimizations:

1. **Efficient data structures**: Using numpy arrays for numerical calculations
2. **Asynchronous WebSocket handling**: Non-blocking I/O for network communication
3. **Buffered updates**: UI updates are throttled to reduce CPU usage
4. **Optimized visualization**: Matplotlib plots are updated efficiently

## Logging

The application includes comprehensive logging with both file and console outputs. Logs are stored in `trade_simulator.log`.

## License

This project is proprietary and confidential.

## Author

Aditya Cherukuru - cherukuru.aditya01@gmail.com
