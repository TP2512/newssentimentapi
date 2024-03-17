from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_url: str
    mongodb_database: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
