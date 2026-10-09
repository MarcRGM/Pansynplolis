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