import time
from typing import Any, Dict, List

class ExecutionTracer:
    """
    Instruments a single HTTP request lifecycle.
    Captures duration, status, and metadata for every architectural hop.
    """
    def __init__(self, endpoint: str):
        self.endpoint: str = endpoint
        self.start_time: float = time.perf_counter() # record starts for duration tracking (checks the current time)
        self.spans: List[Dict[str, Any]] = [] # timed block

    def record_span(
        self, 
        layer: str, 
        operation: str, 
        status: str, 
        details: str, 
        duration_ms: float
    ) -> None:
        """Records an individual execution unit into the trace log."""
        self.spans.append({
            "layer": layer, # GATEWAY | AUTH | CACHE | DATABASE
            "operation": operation, # example like DECODE_TOKEN, QUERY_INDEX
            "status": status, # SUCCESS | HIT | MISS | BLOCKED | ERROR
            "details": details,
            "duration_ms": round(duration_ms, 2)
        })

    def finalize(self) -> Dict[str, Any]:
        """Calculates total end-to-end request duration and returns the completed trace."""
        total_latency_ms = round((time.perf_counter() - self.start_time) * 1000, 2)
        return {
            "endpoint": self.endpoint,
            "total_latency_ms": total_latency_ms,
            "spans": self.spans
        }