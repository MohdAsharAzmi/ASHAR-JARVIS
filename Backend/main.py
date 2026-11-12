from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.brain import generate_reply
from core.agents import agent_manager


app = FastAPI(
    title="Ashar JARVIS",
    description="Personal AI Assistant API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    language: str = "hinglish"
    personality: str = "professional"
    history: list[dict] = Field(default_factory=list)


@app.get("/")
def home():
    return {
        "status": "online",
        "assistant": "ASHAR JARVIS",
        "message": "JARVIS backend is ready"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/agents")
def get_agents():
    agents = agent_manager.list_agents()

    return {
        "status": "success",
        "main_assistant": "ASHAR JARVIS",
        "total_agents": len(agents),
        "available_agents": agents
    }


@app.post("/chat")
def chat(request: ChatRequest):

    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    history = request.history[-10:]

    reply = generate_reply(
        message=message,
        language=request.language,
        personality=request.personality,
        history=history
    )

    return {
        "status": "success",
        "user_message": message,
        "language": request.language,
        "personality": request.personality,
        "history_received": len(history),
        "reply": reply
    }
    
