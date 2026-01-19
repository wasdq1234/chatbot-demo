from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat

app = FastAPI(
    title="RAG Chatbot API",
    description="RAG 기반 대화형 AI Chatbot API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat", tags=["chat"])


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}
