import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Logging
    log_level: str = "INFO"
    
    # API settings
    api_prefix: str = "/api/v1"
    title: str = "Nuranest Pregnancy AI API"
    description: str = "AI-powered pregnancy health information assistant"
    version: str = "1.0.0"
    
    # CORS settings
    cors_origins: list = ["*"]
    cors_methods: list = ["*"]
    cors_headers: list = ["*"]
    
    # AI Model settings
    groq_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None  # Allow this field
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model: str = "llama3-8b-8192"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 2000
    
    # Vectorstore settings
    vectorstore_path: str = "vectorstore_local"
    search_k: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields

# Create settings instance
settings = Settings()

# Load environment variables
if not settings.groq_api_key:
    settings.groq_api_key = os.getenv("GROQ_API_KEY") 