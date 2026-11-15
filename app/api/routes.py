from uuid import uuid4
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field
from app.brain import AssistantBrain
from app.config import get_settings,save_runtime_config
from app.memory import MemoryStore
router=APIRouter()
settings=get_settings()
memory=MemoryStore(settings.database_url.removeprefix("sqlite:///"))
brain=AssistantBrain(settings)
class ChatRequest(BaseModel):
    message:str=Field(min_length=1,max_length=12000)
    conversation_id:str|None=None
class ColabSettings(BaseModel):
    base_url:str=Field(min_length=8,max_length=500)
    chat_path:str="/v1/chat/completions"
    model:str="remoteai-model"
@router.get("/health")
async def health(): return {"status":"ok","app":settings.app_name}
@router.get("/provider/config")
async def provider_config():
    return {"provider":settings.model_provider,"base_url":settings.colab_base_url,"chat_path":settings.colab_chat_path,"model":settings.colab_model}
@router.get("/provider/health")
async def provider_health():
    try: return await brain.provider.health_check()
    except Exception: return {"connected":False,"provider":settings.model_provider,"detail":"Provider check failed."}
@router.put("/provider/colab")
async def update_colab(payload:ColabSettings):
    global brain
    if not payload.base_url.startswith(("https://","http://")): raise HTTPException(400,"URL must begin with http:// or https://")
    saved=save_runtime_config({"colab_base_url":payload.base_url.rstrip("/"),"colab_chat_path":payload.chat_path,"colab_model":payload.model})
    settings.colab_base_url=saved["colab_base_url"]; settings.colab_chat_path=saved["colab_chat_path"]; settings.colab_model=saved["colab_model"]
    brain=AssistantBrain(settings)
    return {"saved":True,"base_url":settings.colab_base_url}
@router.post("/chat")
async def chat(req:ChatRequest):
    cid=req.conversation_id or str(uuid4())
    try:
        result=await brain.respond(req.message,memory.get_messages(cid))
    except Exception as exc:
        raise HTTPException(502,f"Model request failed ({type(exc).__name__}). Check your Colab session and API contract.") from exc
    memory.add_message(cid,"user",req.message); memory.add_message(cid,"assistant",result["response"])
    return {"conversation_id":cid,**result}
@router.get("/memory/facts")
async def facts(): return memory.list_facts()
@router.post("/memory/facts")
async def add_fact(payload:dict):
    fact=str(payload.get("fact","")).strip()
    if not fact: raise HTTPException(400,"fact is required")
    return {"id":memory.add_fact(fact),"fact":fact}
@router.get("/memory/tasks")
async def tasks(): return memory.list_tasks()
@router.post("/memory/tasks")
async def add_task(payload:dict):
    title=str(payload.get("title","")).strip()
    if not title: raise HTTPException(400,"title is required")
    return {"id":memory.add_task(title),"title":title,"status":"pending"}
