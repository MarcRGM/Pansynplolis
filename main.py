import time
from typing import Dict, Any
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.responses import FileResponse

from telemetry import ExecutionTracer
from storage import get_from_cache, set_in_cache, flush_cache, query_database
from security import create_access_token, verify_access_token

app = FastAPI(title="Pansynpolis Telemetry Engine")

@app.get("/")
def serve_dashboard():
    """Serves the single-page visual telemetry dashboard."""
    return FileResponse("index.html")

@app.post("/api/v1/auth/token")
def login_for_access_token(user_id: str = "user_dev_404"):
    """API Gateway & Auth: Generates a signed JWT for testing."""
    tracer = ExecutionTracer("/api/v1/auth/token")

    # Gateway ingress
    t0 = time.perf_counter()
    tracer.record_span(
        "GATEWAY",
        "ROUTE_DISPATCH",
        "SUCCESS",
        f"POST routed to auth controller for {user_id}",
        (time.perf_counter() - t0) * 1000 # convert to ms
    )