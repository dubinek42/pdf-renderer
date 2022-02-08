from pydantic import BaseSettings, Field, PostgresDsn


class RabbitConfig(BaseSettings):
    user: str = Field("dev", env="rabbitmq_default_user")
    password: str = Field("dev", env="rabbitmq_default_pass")
    rabbit_host: str = "rabbit"

    def get_rabbit_url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.rabbit_host}"


class Config(BaseSettings):
    app_name: str = "pdf-renderer"
    debug: bool = False
    db_dsn: PostgresDsn
    path_documents: str = "/documents"
    path_images: str = "/images"
    max_upload_size_bytes: int = 20 * 1000 * 1000  # 20 MB by default
