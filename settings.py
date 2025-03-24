from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MY_EMAIL:str
    MY_PASSWORD:str

    class Config:
        env_file = ".env"  # Load from .env file

# Create a singleton instance
# settings = Settings()
