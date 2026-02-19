from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "患者社区"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置（使用SQLite进行快速测试）
    DATABASE_URL: str = "sqlite:///./patient_community.db"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # 文件上传配置
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # OpenAI配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # CORS配置
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
