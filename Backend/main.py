
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.brain import generate_reply


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


@app.get("/")
def home():
    return {
        "status": "online",
        "assistant": "ASHAR JARVIS",
        "message": "JARVIS backend is ready"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat")
def chat(request: ChatRequest):

    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    reply = generate_reply(
        message,
        request.language,
        request.personality
    )

    return {
        "status": "success",
        "user_message": message,
        "language": request.language,
        "personality": request.personality,
        "reply": reply
    }
    
