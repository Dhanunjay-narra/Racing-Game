import time
from typing import Dict, Any, List
from collections import deque
from backend.core.logger import logger


class TelemetryCollector:
    def __init__(self, max_buffer_size: int = 5000):
        self.buffer: deque = deque(maxlen=max_buffer_size)
        self.metrics_counter: Dict[str, int] = {}
        self.latencies: Dict[str, List[float]] = {}

    def record_event(self, event_name: str, payload: Dict[str, Any]):
        timestamp = time.time()
        record = {
            "name": event_name,
            "timestamp": timestamp,
            "payload": payload
        }
        self.buffer.append(record)
        self.metrics_counter[event_name] = self.metrics_counter.get(event_name, 0) + 1

    def record_latency(self, metric_name: str, latency_ms: float):
        if metric_name not in self.latencies:
            self.latencies[metric_name] = []
        self.latencies[metric_name].append(latency_ms)
        if len(self.latencies[metric_name]) > 1000:
            self.latencies[metric_name].pop(0)

    def get_summary(self) -> Dict[str, Any]:
        avg_latencies = {
            k: (sum(v) / len(v) if v else 0.0)
            for k, v in self.latencies.items()
        }
        return {
            "total_events_buffered": len(self.buffer),
            "event_counts": self.metrics_counter,
            "average_latencies_ms": avg_latencies
        }


telemetry = TelemetryCollector()
