import time
from typing import Any, Dict, Optional

# Simulated PostgreSQL persistent storage (User Accounts & Profiles)
DATABASE_STORE: Dict[str, Dict[str, Any]] = {
     "usr_dev_404": {
        "id": "usr_dev_404",
        "username": "alex_engineer",
        "email": "alex@pansynpolis.internal",
        "tier": "enterprise",
        "rate_limit_per_min": 1000
    }
}

# Simulated Redis in-memory cache
CACHE_STORE: Dict[str, Dict[str, Any]] = {}

def get_from_cache(key: str) -> Dict[str, Any] | None:
    """Simulates a fast Redis in-memory GET operation."""
    return CACHE_STORE.get(key)

def set_in_cache(key: str, value: Dict[str, Any]) -> None:
    """Simulates a Redis SETEX (set-expire) operation storing a key in RAM."""
    CACHE_STORE[key] = value

def flush_cache() -> None:
    """Simulates a Redis FLUSHDB command clearing the cache."""
    CACHE_STORE.clear()

def query_database(record_id: str) -> Dict[str, Any] | None:
    """
    Fetch a record from the database by its ID.
    Simulates a PostgreSQL indexed query with a 25ms disk I/O delay.
    """
    time.sleep(0.025)
    return DATABASE_STORE.get(record_id)

