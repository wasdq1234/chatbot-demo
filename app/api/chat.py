import json

from fastapi import APIRouter
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from app.services.rag import generate_stream

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


async def event_generator(message: str):
    """SSE 이벤트 생성기"""
    async for token in generate_stream(message):
        yield {"data": json.dumps({"token": token})}
    yield {"data": "[DONE]"}


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """RAG 기반 스트리밍 채팅 엔드포인트"""
    return EventSourceResponse(event_generator(request.message))
