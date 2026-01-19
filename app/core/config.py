import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """애플리케이션 설정"""

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma")


settings = Settings()
