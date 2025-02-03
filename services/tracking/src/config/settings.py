from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic: str = "default_topic"

    class Config:
        env_file = ".env"


settings = Settings()
