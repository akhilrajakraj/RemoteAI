from typing import Any
import httpx
from app.providers.base import ModelProvider

class ColabOllamaProvider(ModelProvider):
    """Calls Ollama running inside Google Colab through its Cloudflare tunnel."""
    def __init__(self,base_url:str,model:str="qwen3.5:9b",timeout:float=180,api_key:str|None=None):
        self.base_url=base_url.rstrip("/")
        self.model=model
        self.timeout=timeout
        self.api_key=api_key

    def headers(self)->dict[str,str]:
        headers={"Content-Type":"application/json"}
        if self.api_key:
            headers["Authorization"]=f"Bearer {self.api_key}"
        return headers

    async def generate(self,messages:list[dict[str,str]],**kwargs:Any)->str:
        if not self.base_url:
            raise RuntimeError("Colab is not connected. Start the notebook and paste its Cloudflare URL.")
        payload={
            "model":kwargs.get("model",self.model),
            "messages":messages,
            "stream":False,
            "options":{"temperature":kwargs.get("temperature",0.4)}
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response=await client.post(self.base_url+"/api/chat",json=payload,headers=self.headers())
            response.raise_for_status()
            data=response.json()
        try:
            return str(data["message"]["content"])
        except (KeyError,TypeError) as exc:
            raise RuntimeError("Unexpected Ollama response. Expected message.content from POST /api/chat.") from exc

    async def health_check(self)->dict[str,Any]:
        if not self.base_url:
            return {"connected":False,"provider":"colab-ollama","detail":"Colab tunnel URL is not configured."}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response=await client.get(self.base_url+"/api/tags",headers=self.headers())
                response.raise_for_status()
                data=response.json()
            models=[m.get("name","") for m in data.get("models",[])]
            return {"connected":True,"provider":"colab-ollama","model":self.model,
                    "model_available":any(self.model==name or self.model.split(":")[0]==name.split(":")[0] for name in models),
                    "models":models}
        except (httpx.HTTPError,ValueError,TypeError):
            return {"connected":False,"provider":"colab-ollama","detail":"Cloudflare tunnel or Ollama API is unreachable."}

# Compatibility alias for existing imports.
ColabProvider=ColabOllamaProvider
