from typing import Any, Literal, Optional
from pydantic import BaseModel

class ToolAction(BaseModel):
    type: Literal["tool"]
    name: Literal["list_apis", "get_api", "call_api"]
    args: dict[str, Any] = {}

class FinishAction(BaseModel):
    type: Literal["finish"]

class Step(BaseModel):
    thought: str
    action: ToolAction | FinishAction
    final: Optional[dict[str, Any]] = None
