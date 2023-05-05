from pydantic import BaseSettings


class Settings(BaseSettings):
    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    @property
    def database_url(self):
        user = f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
        database = f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return f'postgresql+asyncpg://{user}@{database}'

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    # Auth
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env.dev"


settings = Settings()
