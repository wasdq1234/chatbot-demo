# Technical Requirements Document (TRD)

## 1. 시스템 아키텍처

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Streamlit     │────▶│    FastAPI      │────▶│   OpenAI API    │
│   (Test UI)     │ SSE │   (Backend)     │     │   (LLM)         │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                        ┌────────▼────────┐
                        │     Chroma      │
                        │   (Vector DB)   │
                        └─────────────────┘
```

---

## 2. 디렉토리 구조

```
chatbot-demo/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱 진입점
│   ├── api/
│   │   ├── __init__.py
│   │   └── chat.py          # /chat/stream 엔드포인트
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # 환경 설정 로드
│   └── services/
│       ├── __init__.py
│       └── rag.py           # RAG 서비스 로직
├── ui/
│   └── streamlit_app.py     # Streamlit 테스트 UI
├── data/
│   └── documents/           # RAG용 문서 저장
├── .env                     # API Key 설정
├── .env.example             # 환경 변수 템플릿
├── pyproject.toml
└── README.md
```

---

## 3. API 명세

### 3.1 POST /chat/stream

채팅 메시지를 받아 RAG 기반 스트리밍 응답 반환

**Request**
```json
{
  "message": "string"
}
```

**Response**
- Content-Type: `text/event-stream`
- SSE 형식으로 토큰 단위 스트리밍

```
data: {"token": "안녕"}

data: {"token": "하세요"}

data: [DONE]
```

---

## 4. 핵심 컴포넌트

### 4.1 RAG Service (`app/services/rag.py`)

| 함수 | 설명 |
|------|------|
| `load_documents()` | 문서 로드 및 청크 분할 |
| `create_vectorstore()` | Chroma 벡터 DB 생성 |
| `get_retriever()` | 문서 검색기 반환 |
| `generate_stream()` | 스트리밍 응답 생성 (async generator) |

### 4.2 Config (`app/core/config.py`)

| 변수 | 설명 |
|------|------|
| `OPENAI_API_KEY` | OpenAI API 키 |
| `CHROMA_PERSIST_DIR` | Chroma DB 저장 경로 |

---

## 5. 환경 설정

### 5.1 .env.example

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 6. 의존성

```toml
[project]
dependencies = [
    "fastapi",
    "uvicorn",
    "langchain",
    "langchain-openai",
    "chromadb",
    "python-dotenv",
    "streamlit",
    "sse-starlette",
]
```

---

## 7. 실행 방법

### Backend
```bash
uvicorn app.main:app --reload
```

### Streamlit UI
```bash
streamlit run ui/streamlit_app.py
```
