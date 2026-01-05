from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False

    class ConfigDict:
        env_file = ".env"
        extra = "allow"


settings = Settings()
