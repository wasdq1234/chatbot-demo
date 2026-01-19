from collections.abc import AsyncGenerator
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings

PROMPT_TEMPLATE = """다음 컨텍스트를 참고하여 질문에 답변하세요.

컨텍스트:
{context}

질문: {question}

답변:"""


def load_documents(directory: str = "./data/documents") -> list[Document]:
    """문서를 로드하고 청크로 분할합니다.

    Args:
        directory: 문서가 저장된 디렉토리 경로

    Returns:
        분할된 Document 리스트
    """
    path = Path(directory)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        return []

    loader = DirectoryLoader(
        directory,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()

    if not documents:
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_documents(documents)

    return chunks


def create_vectorstore(documents: list[Document]) -> Chroma:
    """문서로부터 Chroma 벡터 스토어를 생성합니다.

    Args:
        documents: 임베딩할 Document 리스트

    Returns:
        Chroma 벡터 스토어 인스턴스
    """
    embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=settings.CHROMA_PERSIST_DIR,
    )

    return vectorstore


def get_retriever() -> VectorStoreRetriever:
    """Chroma 벡터 스토어에서 retriever를 반환합니다.

    기존 벡터 스토어가 있으면 로드하고, 없으면 새로 생성합니다.

    Returns:
        VectorStoreRetriever 인스턴스
    """
    embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
    persist_path = Path(settings.CHROMA_PERSIST_DIR)

    if persist_path.exists() and any(persist_path.iterdir()):
        vectorstore = Chroma(
            persist_directory=settings.CHROMA_PERSIST_DIR,
            embedding_function=embeddings,
        )
    else:
        documents = load_documents()
        if not documents:
            raise ValueError("문서가 없습니다. data/documents/ 폴더에 문서를 추가하세요.")
        vectorstore = create_vectorstore(documents)

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )

    return retriever


async def generate_stream(message: str) -> AsyncGenerator[str, None]:
    """RAG 기반 스트리밍 응답을 생성합니다.

    Args:
        message: 사용자 질문

    Yields:
        토큰 단위 응답 문자열
    """
    retriever = get_retriever()
    docs = retriever.invoke(message)
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    formatted_prompt = prompt.format(context=context, question=message)

    llm = ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        model="gpt-4o-mini",
        streaming=True,
    )

    async for chunk in llm.astream(formatted_prompt):
        if chunk.content:
            yield chunk.content
