import time
import threading
from collections import deque
import numpy as np

class PerformanceMonitor:
    def __init__(self, window_size=1000):
        self.processing_times = deque(maxlen=window_size)
        self.ui_update_times = deque(maxlen=window_size)
        self.network_latencies = deque(maxlen=window_size)
        self.lock = threading.Lock()
        
    def record_processing_time(self, start_time):
        with self.lock:
            self.processing_times.append(time.time() - start_time)
    
    def record_ui_update(self, duration):
        with self.lock:
            self.ui_update_times.append(duration)
    
    def record_network_latency(self, server_time):
        with self.lock:
            self.network_latencies.append(time.time() - server_time)
    
    def get_metrics(self):
        with self.lock:
            metrics = {
                "avg_processing_time": np.mean(self.processing_times) if self.processing_times else 0,
                "max_processing_time": np.max(self.processing_times) if self.processing_times else 0,
                "avg_ui_latency": np.mean(self.ui_update_times) if self.ui_update_times else 0,
                "avg_network_latency": np.mean(self.network_latencies) if self.network_latencies else 0,
                "messages_per_second": len(self.processing_times) / (time.time() - time.time())
            }
        return metrics