from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 45
    database_url: str
    default_admin_email: str
    default_admin_password: str
    admin_email: str
    admin_password: str

    class Config:
        env_file = ".env"

settings = Settings()

