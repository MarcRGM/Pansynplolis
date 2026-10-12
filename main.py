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

    # Layer 1 - Gateway ingress
    t_start = time.perf_counter()
    tracer.record_span(
        "GATEWAY",
        "ROUTE_DISPATCH",
        "SUCCESS",
        f"POST routed to auth controller for {user_id}",
        (time.perf_counter() - t_start) * 1000 # convert to ms
    )

    # Layer 2 - Auth sign-in
    t_auth = time.perf_counter()
    token = create_access_token(subject=user_id)
    tracer.record_span(
        "AUTH", 
        "SIGN_JWT", 
        "SUCCESS", 
        "Generated 256-bit signed token", 
        (time.perf_counter() - t_auth) * 1000
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "telemetry": tracer.finalize()
    }

@app.get("/api/v1/users/{user_id}/profile")
def get_user_profile(user_id: str, authorization: str | None = Header(None)): # Let FastAPI know authorization is in Header
    """Full-stack request lifecycle with execution tracing"""
    tracer = ExecutionTracer(f"/api/users/{user_id}/profile")

    # Layer 1 - Gateway ingress
    t_start = time.perf_counter()
    tracer.record_span(
        "GATEWAY",
        "INGRESS_HTTP",
        "SUCCESS",
        f"Received GET request for user {user_id}",
        (time.perf_counter() - t_start) * 1000
    )

    # Layer 2 - Auth validation
    t_auth = time.perf_counter()
    # Missing or malformed atuh header
    if not authorization or not authorization.startswith("Bearer "):
        tracer.record_span(
            "AUTH",
            "VERIFY_TOKEN",
            "BLOCKED",
            "Missing or malformed Authorization header",
            (time.perf_counter() - t_auth) * 1000
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Unauthorizzed", "telemetry": tracer.finalize()}  
        )

    token = authorization.split(" ")[1] # take only the token ([0] = "Bearer", [1] = token string)
    is_valid, claims, reason = verify_access_token(token)
    if not is_valid:
        tracer.record_span(
            "AUTH",
            "VERIFY_TOKEN",
            "BLOCKED",
            reason,
            (time.perf_counter() - t_auth) * 1000
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Unauthorizzed", "telemetry": tracer.finalize()}
        )

    # Success
    tracer.record_span(
        "AUTH",
        "VERIFY_TOKEN",
        "SUCCESS",
        f"Authenticated subject: {claims.get('sub')}",
        (time.perf_counter() - t_auth) * 1000
    )
    
    # Layer 3 - Cache (Redis)
    t_cache = time.perf_counter()
    cached_record = get_from_cache(user_id)
    cache_duration = (time.perf_counter() - t_cache) * 1000

    if cached_record:
        tracer.record_span(
            "CACHE",
            "REDIS_GET",
            "HIT",
            f"Retrieved profile from in-memory key: {user_id}",
            cache_duration
        )
        return {
            "source": "REDIS_CACHE_HIT",
            "data": cached_record,
            "telemetry": tracer.finalize()
        }

    tracer.record_span(
        "CACHE",
        "REDIS_GET",
        "MISS",
        f"Key not present in cache: {user_id}"
    )