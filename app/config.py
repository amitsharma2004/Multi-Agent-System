from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Keys
    tavily_api_key: str
    firecrawl_api_key: str
    
    # MongoDB
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "sales_outreach_db"
    
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"


settings = Settings()
