from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.brain import AssistantBrain
from app.config import get_settings
from app.memory import MemoryStore

router = APIRouter()
settings = get_settings()
memory = MemoryStore(settings.database_url.removeprefix("sqlite:///"))
brain = AssistantBrain(settings)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    conversation_id: str
    response: str


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    conversation_id = request.conversation_id or str(uuid4())
    history = memory.get_messages(conversation_id)
    memory.add_message(conversation_id, "user", request.message)
    try:
        answer = await brain.respond(request.message, history)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Model request failed: {exc}") from exc
    memory.add_message(conversation_id, "assistant", answer)
    return ChatResponse(conversation_id=conversation_id, response=answer)


@router.get("/memory/facts")
async def facts():
    return memory.list_facts()


@router.post("/memory/facts")
async def create_fact(payload: dict):
    fact = str(payload.get("fact", "")).strip()
    if not fact:
        raise HTTPException(status_code=400, detail="fact is required")
    return {"id": memory.add_fact(fact), "fact": fact}


@router.get("/memory/tasks")
async def tasks():
    return memory.list_tasks()


@router.post("/memory/tasks")
async def create_task(payload: dict):
    title = str(payload.get("title", "")).strip()
    if not title:
        raise HTTPException(status_code=400, detail="title is required")
    return {"id": memory.add_task(title), "title": title, "status": "pending"}
