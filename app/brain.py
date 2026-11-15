from app.config import Settings
from app.providers.factory import get_provider
from app.agents.orchestrator import MultiAgentOrchestrator
class AssistantBrain:
    def __init__(self,settings:Settings):
        self.settings=settings
        self.provider=get_provider(settings)
        self.orchestrator=MultiAgentOrchestrator(self.provider,settings.agent_max_parallel)
    async def respond(self,prompt:str,history:list[dict[str,str]]|None=None)->dict:
        if not prompt.strip(): raise ValueError("Prompt cannot be empty")
        return await self.orchestrator.run(prompt,history)
