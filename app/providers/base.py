from abc import ABC, abstractmethod

class ModelProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, history: list[dict[str, str]]) -> str:
        raise NotImplementedError
