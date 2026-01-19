# MVP 개발 태스크

## Phase 1: 프로젝트 초기 설정

### Task 1.1: 디렉토리 구조 생성
- [x] `app/` 디렉토리 생성
- [x] `app/__init__.py` 생성
- [x] `app/api/` 디렉토리 생성
- [x] `app/api/__init__.py` 생성
- [x] `app/core/` 디렉토리 생성
- [x] `app/core/__init__.py` 생성
- [x] `app/services/` 디렉토리 생성
- [x] `app/services/__init__.py` 생성
- [x] `ui/` 디렉토리 생성
- [x] `data/documents/` 디렉토리 생성

### Task 1.2: 의존성 설정
- [x] `pyproject.toml`에 의존성 추가
  ```toml
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
- [x] `uv sync` 실행하여 패키지 설치

### Task 1.3: 환경 설정 파일 생성
- [x] `.env.example` 파일 생성
  ```env
  OPENAI_API_KEY=your_openai_api_key_here
  ```
- [x] `.env` 파일 생성 (실제 API 키 입력)
- [x] `.gitignore`에 `.env` 추가

---

## Phase 2: Core 모듈 개발

### Task 2.1: Config 모듈 구현 (`app/core/config.py`)
- [x] python-dotenv를 사용한 환경 변수 로드
- [x] `Settings` 클래스 구현
  ```python
  class Settings:
      OPENAI_API_KEY: str
      CHROMA_PERSIST_DIR: str = "./data/chroma"
  ```
- [x] settings 인스턴스 export

**파일 위치**: `app/core/config.py`

**구현 내용**:
- `load_dotenv()` 호출
- 환경 변수에서 `OPENAI_API_KEY` 로드
- Chroma DB 저장 경로 설정

---

## Phase 3: RAG 서비스 개발

### Task 3.1: 문서 로드 함수 구현 (`app/services/rag.py`)
- [x] `load_documents()` 함수 구현
  - `data/documents/` 경로에서 문서 로드
  - LangChain `TextLoader` 또는 `DirectoryLoader` 사용
  - `RecursiveCharacterTextSplitter`로 청크 분할
  - chunk_size: 1000, chunk_overlap: 200

**입력**: 문서 디렉토리 경로
**출력**: `List[Document]`

### Task 3.2: 벡터 스토어 생성 함수 구현
- [x] `create_vectorstore()` 함수 구현
  - OpenAI Embeddings 사용
  - Chroma 벡터 DB 생성
  - persist_directory 설정으로 영구 저장

**입력**: `List[Document]`
**출력**: `Chroma` 인스턴스

### Task 3.3: Retriever 함수 구현
- [x] `get_retriever()` 함수 구현
  - 기존 Chroma DB 로드 또는 새로 생성
  - `as_retriever()` 메서드로 retriever 반환
  - search_kwargs: k=3 (상위 3개 문서 검색)

**출력**: `VectorStoreRetriever`

### Task 3.4: 스트리밍 응답 생성 함수 구현
- [x] `generate_stream()` async generator 함수 구현
  - 사용자 메시지 입력 받음
  - retriever로 관련 문서 검색
  - ChatOpenAI 모델 사용 (streaming=True)
  - 프롬프트 템플릿 구성 (context + question)
  - 토큰 단위로 yield

**입력**: `message: str`
**출력**: `AsyncGenerator[str, None]`

**프롬프트 템플릿 예시**:
```
다음 컨텍스트를 참고하여 질문에 답변하세요.

컨텍스트:
{context}

질문: {question}

답변:
```

---

## Phase 4: FastAPI 백엔드 개발

### Task 4.1: FastAPI 앱 설정 (`app/main.py`)
- [ ] FastAPI 앱 인스턴스 생성
- [ ] CORS 미들웨어 설정 (Streamlit 연동용)
- [ ] chat 라우터 등록
- [ ] health check 엔드포인트 추가 (`GET /health`)

### Task 4.2: Chat API 엔드포인트 구현 (`app/api/chat.py`)
- [ ] `ChatRequest` Pydantic 모델 정의
  ```python
  class ChatRequest(BaseModel):
      message: str
  ```
- [ ] `POST /chat/stream` 엔드포인트 구현
  - `ChatRequest` 입력 받음
  - `sse_starlette.sse.EventSourceResponse` 사용
  - RAG 서비스의 `generate_stream()` 호출
  - SSE 형식으로 응답 스트리밍

**응답 형식**:
```
data: {"token": "텍스트"}

data: [DONE]
```

### Task 4.3: 라우터 연결
- [ ] `app/api/__init__.py`에서 chat 라우터 export
- [ ] `app/main.py`에서 라우터 include

---

## Phase 5: Streamlit UI 개발

### Task 5.1: Streamlit 채팅 UI 구현 (`ui/streamlit_app.py`)
- [ ] 페이지 설정 (title, layout)
- [ ] 채팅 히스토리 session_state 관리
- [ ] 채팅 입력창 구현 (`st.chat_input`)
- [ ] 채팅 메시지 표시 (`st.chat_message`)
- [ ] FastAPI 스트리밍 API 호출
  - `requests` 또는 `httpx`로 SSE 스트리밍 처리
  - 실시간 토큰 표시 (`st.write_stream` 또는 placeholder)

**UI 구성**:
```
┌─────────────────────────────┐
│  RAG Chatbot               │
├─────────────────────────────┤
│  [User]: 질문 내용          │
│  [Assistant]: 답변 내용...  │
│                             │
├─────────────────────────────┤
│  [메시지 입력창]            │
└─────────────────────────────┘
```

---

## Phase 6: 테스트 및 검증

### Task 6.1: 테스트 문서 준비
- [ ] `data/documents/`에 샘플 문서 추가
- [ ] 문서 임베딩 및 벡터 DB 생성 확인

### Task 6.2: API 테스트
- [ ] FastAPI 서버 실행 (`uvicorn app.main:app --reload`)
- [ ] `/health` 엔드포인트 확인
- [ ] `/chat/stream` 엔드포인트 curl 테스트
  ```bash
  curl -X POST http://localhost:8000/chat/stream \
    -H "Content-Type: application/json" \
    -d '{"message": "테스트 질문"}'
  ```

### Task 6.3: E2E 테스트
- [ ] Streamlit UI 실행 (`streamlit run ui/streamlit_app.py`)
- [ ] 채팅 입력 및 스트리밍 응답 확인
- [ ] 여러 턴 대화 테스트

---

## 체크리스트 요약

| Phase | Task | 상태 |
|-------|------|------|
| 1 | 디렉토리 구조 생성 | [x] |
| 1 | 의존성 설정 | [x] |
| 1 | 환경 설정 파일 생성 | [x] |
| 2 | Config 모듈 구현 | [x] |
| 3 | 문서 로드 함수 구현 | [x] |
| 3 | 벡터 스토어 생성 함수 구현 | [x] |
| 3 | Retriever 함수 구현 | [x] |
| 3 | 스트리밍 응답 생성 함수 구현 | [x] |
| 4 | FastAPI 앱 설정 | [ ] |
| 4 | Chat API 엔드포인트 구현 | [ ] |
| 4 | 라우터 연결 | [ ] |
| 5 | Streamlit 채팅 UI 구현 | [ ] |
| 6 | 테스트 문서 준비 | [ ] |
| 6 | API 테스트 | [ ] |
| 6 | E2E 테스트 | [ ] |
