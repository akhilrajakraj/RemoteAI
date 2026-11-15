from typing import Any
import httpx
from app.providers.base import ModelProvider
class ColabProvider(ModelProvider):
    """OpenAI-compatible adapter for a model server exposed from Google Colab."""
    def __init__(self,base_url:str,chat_path:str="/v1/chat/completions",model:str="remoteai-model",api_key:str|None=None,timeout:float=120):
        self.base_url=base_url.rstrip("/")
        self.chat_path="/"+chat_path.lstrip("/")
        self.model,self.api_key,self.timeout=model,api_key,timeout
    def headers(self):
        h={"Content-Type":"application/json"}
        if self.api_key: h["Authorization"]=f"Bearer {self.api_key}"
        return h
    async def generate(self,messages:list[dict[str,str]],**kwargs:Any)->str:
        if not self.base_url: raise RuntimeError("Colab URL is not configured. Add your active tunnel URL in RemoteAI settings.")
        payload={"model":kwargs.get("model",self.model),"messages":messages,"temperature":kwargs.get("temperature",0.4)}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response=await client.post(self.base_url+self.chat_path,json=payload,headers=self.headers())
            response.raise_for_status()
            data=response.json()
        try: return str(data["choices"][0]["message"]["content"])
        except (KeyError,IndexError,TypeError) as exc:
            raise RuntimeError("Colab response must contain choices[0].message.content. Adapt this provider to your notebook API.") from exc
    async def health_check(self)->dict[str,Any]:
        if not self.base_url: return {"connected":False,"provider":"colab","detail":"Colab URL is not configured."}
        async with httpx.AsyncClient(timeout=8) as client:
            for path in ("/health","/"):
                try:
                    r=await client.get(self.base_url+path,headers=self.headers())
                    if r.is_success: return {"connected":True,"provider":"colab","url":self.base_url}
                except httpx.HTTPError: pass
        return {"connected":False,"provider":"colab","url":self.base_url,"detail":"Tunnel is unreachable or has no health/root endpoint."}
