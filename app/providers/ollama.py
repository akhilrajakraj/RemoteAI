import httpx
from app.providers.base import ModelProvider

class OllamaProvider(ModelProvider):
    def __init__(self, base_url: str, model: str) -> None:
        self.base_url, self.model = base_url.rstrip("/"), model

    async def generate(self, prompt: str, history: list[dict[str, str]]) -> str:
        messages = [{"role": m["role"], "content": m["content"]} for m in history if m.get("role") in {"user", "assistant"}]
        messages.append({"role": "user", "content": prompt})
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(f"{self.base_url}/api/chat", json={"model": self.model, "messages": messages, "stream": False})
            response.raise_for_status()
            data = response.json()
        return data.get("message", {}).get("content", "The model returned an empty response.")
