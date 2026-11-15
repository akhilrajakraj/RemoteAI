import httpx

from app.providers.base import ModelProvider


class RemoteProvider(ModelProvider):
    def __init__(self, endpoint: str, api_key: str | None = None) -> None:
        self.endpoint = endpoint
        self.api_key = api_key

    async def generate(self, prompt: str, history: list[dict[str, str]]) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                self.endpoint,
                json={"prompt": prompt, "history": history},
                headers=headers,
            )
            response.raise_for_status()
            payload = response.json()
        return str(payload.get("response", payload.get("text", "")))
