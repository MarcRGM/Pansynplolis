import time
from typing import Any, Dict, List

class ExecutionTracer:
    """
    Instruments a single HTTP request lifecycle.
    Captures duration, status, and metadata for every architectural hop.
    """
    def __init__(self, endpoint: str):
        self.endpoint: str = endpoint
        self.start_time: float = time.perf_counter() # record starts for duration tracking
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
            "layer": layer,            # GATEWAY | AUTH | CACHE | DATABASE
            "operation": operation,    # e.g., DECODE_TOKEN, QUERY_INDEX
            "status": status,          # SUCCESS | HIT | MISS | BLOCKED | ERROR
            "details": details,
            "duration_ms": round(duration_ms, 2)
        })