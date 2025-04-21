from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MY_EMAIL: str
    MY_PASSWORD: str
    OPENAI_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
