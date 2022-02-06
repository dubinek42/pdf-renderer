from pydantic import BaseSettings, PostgresDsn


class Config(BaseSettings):
    app_name: str = "pdf-renderer"
    debug: bool = False
    db_dsn: PostgresDsn
    path_documents: str = "/documents"
    path_images: str = "/images"
