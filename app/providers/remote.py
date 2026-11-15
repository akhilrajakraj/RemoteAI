import httpx
from app.providers.base import ModelProvider

class RemoteProvider(ModelProvider):
    def __init__(self, endpoint: str, api_key: str | None = None) -> None:
        self.endpoint, self.api_key = endpoint, api_key

    async def generate(self, prompt: str, history: list[dict[str, str]]) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(self.endpoint, json={"prompt": prompt, "history": history}, headers=headers)
            response.raise_for_status()
            data = response.json()
        return str(data.get("response", data.get("text", "")))
