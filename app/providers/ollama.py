from typing import Any
import httpx
from app.providers.base import ModelProvider
class OllamaProvider(ModelProvider):
    def __init__(self,base_url:str="http://localhost:11434",model:str="gemma:2b"): self.base_url,self.model=base_url.rstrip("/"),model
    async def generate(self,messages:list[dict[str,str]],**kwargs:Any)->str:
        async with httpx.AsyncClient(timeout=120) as c:
            r=await c.post(self.base_url+"/api/chat",json={"model":self.model,"messages":messages,"stream":False})
            r.raise_for_status()
            return str(r.json().get("message",{}).get("content",""))
    async def health_check(self)->dict[str,Any]:
        try:
            async with httpx.AsyncClient(timeout=5) as c: r=await c.get(self.base_url+"/api/tags"); r.raise_for_status()
            return {"connected":True,"provider":"ollama"}
        except httpx.HTTPError: return {"connected":False,"provider":"ollama"}
