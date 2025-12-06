from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # General
    APP_NAME: str = "FastAPI Clean Architecture"
    DEBUG: bool = True
    API_VERSION: str = "v1"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()