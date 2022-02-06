from dependency_injector import containers, providers

from .db import repositories
from .db.sessions import SessionFactory
from .settings import Config


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(Config)
    session_factory = providers.Singleton(SessionFactory, db_dsn=config.provided.db_dsn)
    document_repository = providers.Factory(
        repositories.Document, open_session=session_factory.provided.open_session
    )
    processed_image_repository = providers.Factory(
        repositories.ProcessedImage, open_session=session_factory.provided.open_session
    )
