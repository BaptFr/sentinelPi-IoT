from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 45
    DATABASE_URL: str
    DEFAULT_ADMIN_EMAIL: str
    DEFAULT_ADMIN_PASSWORD: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    API_URL: str
    RASPBERRY_URL: str
    DEVICE_ID:str

    class Config:
        env_file = ".env"
        extra = "forbid"

settings = Settings()

