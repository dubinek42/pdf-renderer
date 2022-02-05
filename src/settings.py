from pydantic import BaseSettings, PostgresDsn


class Config(BaseSettings):
    app_name: str = "pdf-renderer"
    db_dsn: PostgresDsn
