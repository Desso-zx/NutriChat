from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Central configuration for the NutriChat backend"""

    vector_db_path: str = "./data/vector_db"

    collection_name: str = "nutrichat_knowledge"

    embedding_model: str = "all-MiniLM-L6-v2"

    llm_model: str = "llama3.2"

    top_k: int = 4

    frontend_url: str = "http://localhost:8501"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()