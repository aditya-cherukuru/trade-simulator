# trade_simulator/network/websocket_client.py
import json
import time
import asyncio
import threading
import websockets
import logging

from ..utils.logger import setup_logger

class WebSocketClient:
    """
    Class for handling WebSocket connection and data processing
    """
    def __init__(self, uri, callback):
        self.uri = uri
        self.callback = callback
        self.running = False
        self.ws = None
        self.connection_thread = None
        self.last_tick_time = time.time()
        self.processing_times = []
        self.logger = setup_logger("WebSocketClient")
    
    async def connect(self):
        """Connect to WebSocket and process messages"""
        try:
            self.logger.info(f"Connecting to {self.uri}")
            async with websockets.connect(self.uri) as websocket:
                self.ws = websocket
                self.logger.info("Connected to WebSocket server")
                
                while self.running:
                    try:
                        message = await websocket.recv()
                        start_time = time.time()
                        
                        # Process the message
                        data = json.loads(message)
                        self.callback(data)
                        
                        # Calculate processing time
                        processing_time = time.time() - start_time
                        self.processing_times.append(processing_time)
                        if len(self.processing_times) > 100:
                            self.processing_times.pop(0)
                            
                        self.last_tick_time = time.time()
                    except websockets.exceptions.ConnectionClosed:
                        self.logger.warning("WebSocket connection closed, attempting to reconnect...")
                        break
                    except json.JSONDecodeError:
                        self.logger.error("Failed to decode JSON message")
                    except Exception as e:
                        self.logger.error(f"Error processing WebSocket message: {e}")
        except Exception as e:
            self.logger.error(f"WebSocket connection error: {e}")
            
        # Try to reconnect after a brief delay if still running
        if self.running:
            self.logger.info("Attempting to reconnect in 5 seconds...")
            await asyncio.sleep(5)
            asyncio.create_task(self.connect())
    
    def start(self):
        """Start the WebSocket client in a separate thread"""
        if self.running:
            return
            
        self.running = True
        
        def run_async_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.connect())
        
        self.connection_thread = threading.Thread(target=run_async_loop)
        self.connection_thread.daemon = True
        self.connection_thread.start()
        
    def stop(self):
        """Stop the WebSocket client"""
        self.running = False
        if self.ws:
            asyncio.run(self.ws.close())
        if self.connection_thread:
            self.connection_thread.join(timeout=1)
    
    @property
    def average_processing_time(self):
        """Calculate average processing time per tick"""
        if not self.processing_times:
            return 0
        return sum(self.processing_times) / len(self.processing_times)