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