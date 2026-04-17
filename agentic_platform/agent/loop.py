import json
from pydantic import ValidationError

from agentic_platform.agent.prompt import SYSTEM
from agentic_platform.agent.schemas import Step
from agentic_platform.tracing import Tracer
from agentic_platform.llm.base import LLM
from agentic_platform.tools.api_catalog import list_apis, get_api, call_api

TOOL_MAP = {
    "list_apis": list_apis,
    "get_api": get_api,
    "call_api": call_api,
}

class AgentLoop:
    def __init__(self, llm: LLM, tracer: Tracer, max_steps: int = 8):
        self.llm = llm
        self.tracer = tracer
        self.max_steps = max_steps

    def run(self, task: str) -> dict:
        observation = None
        used_sources: list[str] = []

        for i in range(1, self.max_steps + 1):
            user = (
                f"TASK:\n{task}\n\n"
                f"LAST_OBSERVATION:\n{json.dumps(observation, ensure_ascii=False) if observation else 'null'}"
            )

            raw = self.llm.generate(SYSTEM, user)
            self.tracer.add("llm_raw", step=i, raw=raw)

            try:
                clean = raw.strip()
                if clean.startswith("```"):
                    clean = "\n".join(clean.split("\n")[1:])
                if clean.endswith("```"):
                    clean = "\n".join(clean.split("\n")[:-1])
                clean = clean.strip()
                data = json.loads(clean)
                step = Step.model_validate(data)
            except (json.JSONDecodeError, ValidationError) as e:
                observation = {"error": "invalid_llm_json", "details": str(e), "raw": raw[:3000]}
                self.tracer.add("parse_error", step=i, error=str(e))
                continue

            self.tracer.add("step", step=i, parsed=step.model_dump())

            if step.action.type == "finish":
                final = step.final or {}
                final.setdefault("sources", used_sources)
                self.tracer.add("finish", step=i, final=final)
                return final

            tool_name = step.action.name
            args = step.action.args or {}

            try:
                result = TOOL_MAP[tool_name](**args)
                if isinstance(result, dict) and "url" in result and isinstance(result["url"], str):
                    used_sources.append(result["url"])
                observation = {"tool": tool_name, "args": args, "result": result}
                self.tracer.add("tool_result", step=i, tool=tool_name, result=result)
            except Exception as e:
                observation = {"tool": tool_name, "args": args, "error": str(e)}
                self.tracer.add("tool_error", step=i, tool=tool_name, error=str(e))

        return {"error": "max_steps_reached", "note": "Agent did not finish within the step limit.", "sources": used_sources}
