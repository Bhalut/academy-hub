from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str
    kafka_bootstrap_servers: str
    kafka_topic: str

    class Config:
        env_file = ".env"


settings = Settings()
