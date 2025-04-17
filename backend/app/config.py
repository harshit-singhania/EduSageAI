from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv
import os
from typing import List 

load_dotenv(find_dotenv())

class Settings(BaseSettings):
    # api settings
    API_V1_STR: str = "/api/v1"
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Learning Assistant"
    
    # CORS 
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://localhost:3000"
    ]
    
    # api keys
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
    # openrouter specific settings 
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL_NAME: str = os.getenv("OPENROUTER_MODEL_NAME")
    
    # pinecone database settings 
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    
    class Config: 
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    

settings = Settings()