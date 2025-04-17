from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv
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
    OPENROUTER_API_KEY: str = load_dotenv("OPENROUTER_API_KEY")
    OPENAI_API_KEY: str = load_dotenv("OPENAI_API_KEY")
    
    # pinecone database settings 
    PINECONE_API_KEY: str = load_dotenv("PINECONE_API_KEY")
    
    class Config: 
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    

settings = Settings()