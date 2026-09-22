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