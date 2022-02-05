from dependency_injector import containers, providers

from .db.repositories.document import DocumentRepository
from .db.sessions import SessionFactory
from .settings import Config


class Container(containers.DeclarativeContainer):
    config = Config()
    session_factory = providers.Singleton(SessionFactory, db_dsn=config.db_dsn)

    document_repository = providers.Factory(
        DocumentRepository, open_session=session_factory.provided.open_session
    )
