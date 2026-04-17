from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    def generate(self, system: str, user: str) -> str:
        raise NotImplementedError
