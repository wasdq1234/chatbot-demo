# 프로젝트 요구사항 (MVP)

## 1. 프로젝트 개요

- RAG 기반 대화형 AI Chatbot MVP 개발

---

## 2. 핵심 기능

- [ ] RAG 시스템 구축 (문서 검색 + LLM 응답 생성)
- [ ] FastAPI Streaming Response API 구현

---

## 3. 구현 내용

### 3.1 RAG 시스템
- 벡터 데이터베이스 구축
- 문서 임베딩 및 검색
- LLM 응답 생성

### 3.2 Streaming API
- `/chat/stream` 엔드포인트
- SSE 기반 토큰 스트리밍

### 3.3 환경 설정
- `.env` 파일로 API Key 관리

### 3.4 테스트 UI
- Streamlit 기반 채팅 UI

---

## 4. 기술 스택

| 분류 | 기술 |
|------|------|
| Language | Python |
| LLM | LangChain, OpenAI API |
| Vector DB | Chroma |
| Backend | FastAPI |
| Database | SQLite |
| Config | python-dotenv |
| UI | Streamlit |
