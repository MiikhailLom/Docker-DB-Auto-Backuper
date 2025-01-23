from pydantic_settings import BaseSettings


class StorageConfig(BaseSettings):
    HOST: str
    KEY: str
    PORT: int | None = 22
    USER: str | None = 'root'
    KEY_PASSPHRASE: str | None = ''

    class Config:
        env_prefix = 'STORAGE_'
        env_file = '.env'
        extra = 'ignore'


class DockerConfig(BaseSettings):
    HOST: str

    class Config:
        env_prefix = 'DOCKER_'
        env_file = '.env'
        extra = 'ignore'


class SchedulerConfig(BaseSettings):
    DAYS: int

    class Config:
        env_prefix = 'SCHEDULER_'
        env_file = '.env'
        extra = 'ignore'


class Settings:
    storage = StorageConfig()
    docker = DockerConfig()
    scheduler = SchedulerConfig()


settings = Settings()
