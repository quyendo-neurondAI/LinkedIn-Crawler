from pathlib import Path
from pydantic_settings import BaseSettings

ENV_PATH = Path(__file__).parent.parent

class Settings(BaseSettings):
    LINKEDIN_USERNAME: str
    LINKEDIN_PASSWORD: str
    COOKIE_PATH: str
    # Add other settings here as needed

    class Config:
        env_file = str(ENV_PATH.joinpath(Path(r".env")))

settings = Settings()