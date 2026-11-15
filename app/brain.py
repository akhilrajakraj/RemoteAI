"""Assistant orchestration boundary.

The first version supports a provider-backed chat response. Tool execution will
be routed through an explicit allow-listed registry in a later milestone.
"""
from app.config import Settings
from app.providers.factory import get_provider


class AssistantBrain:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.provider = get_provider(settings)

    async def respond(self, prompt: str, history: list[dict[str, str]] | None = None) -> str:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        return await self.provider.generate(prompt=prompt, history=history or [])
