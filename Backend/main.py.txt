
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
