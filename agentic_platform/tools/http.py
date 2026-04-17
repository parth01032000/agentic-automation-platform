import requests

def http_get(url: str, timeout_s: int = 20) -> dict:
    r = requests.get(url, timeout=timeout_s, headers={"User-Agent": "agentic-platform/0.1"})
    return {
        "url": url,
        "status_code": r.status_code,
        "text": r.text[:20000]
    }
