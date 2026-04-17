import os
import requests
from agentic_platform.llm.base import LLM

class OllamaLLM(LLM):
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    def generate(self, system: str, user: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False
        }
        r = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=120)
        r.raise_for_status()
        return r.json()["message"]["content"]
