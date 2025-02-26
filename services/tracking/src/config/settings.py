from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic: str = "default_topic"
    redis_host: str = "redis"
    redis_port: int = 6379

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
