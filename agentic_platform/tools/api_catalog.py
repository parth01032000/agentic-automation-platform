import json
from pathlib import Path
from urllib.parse import urlencode

from agentic_platform.tools.http import http_get

CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "api_catalog.json"

def list_apis(category: str | None = None) -> dict:
    items = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    if category:
        items = [i for i in items if i.get("category", "").lower() == category.lower()]
    return {"count": len(items), "results": items}

def get_api(name: str) -> dict:
    items = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    for i in items:
        if i["name"].lower() == name.lower():
            return i
    return {"error": f"API not found: {name}"}

def call_api(name: str, params: dict | None = None) -> dict:
    api = get_api(name)
    if "error" in api:
        return api

    if api.get("auth_required"):
        return {
            "error": "auth_required",
            "message": f"{name} requires an API key. This demo keeps calls free by default.",
            "docs_url": api.get("docs_url"),
            "required_env": api.get("auth_env")
        }

    base_url = api["base_url"]
    params = params or {}
    url = base_url + ("?" + urlencode(params) if params else "")
    return http_get(url)
