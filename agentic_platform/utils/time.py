from datetime import datetime, timezone

def run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
