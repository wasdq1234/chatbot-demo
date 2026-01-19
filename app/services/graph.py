"""LangGraph 기반 RAG 그래프 정의"""

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph

from app.services.rag import get_retriever

from app.core.config import settings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

PROMPT_TEMPLATE = """다음 컨텍스트를 참고하여 질문에 답변하세요.

컨텍스트:
{context}

질문: {question}

답변:"""


class RAGState(TypedDict):
    """RAG 그래프 상태"""

    question: str
    context: str
    answer: str


def retrieve_node(state: RAGState) -> dict:
    """문서 검색 노드"""
    retriever = get_retriever()
    docs = retriever.invoke(state["question"])
    context = "\n\n".join(doc.page_content for doc in docs)
    return {"context": context}


def generate_node(state: RAGState) -> dict:
    """응답 생성 노드"""
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    formatted_prompt = prompt.format(
        context=state["context"], question=state["question"]
    )

    llm = ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        model="gpt-4o-mini",
    )

    response = llm.invoke(formatted_prompt)
    return {"answer": response.content}


# StateGraph 빌더 생성
builder = StateGraph(RAGState)

# 노드 추가
builder.add_node("retrieve", retrieve_node)
builder.add_node("generate", generate_node)

# 엣지 정의
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

# 그래프 컴파일
graph = builder.compile()
