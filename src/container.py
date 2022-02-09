from dependency_injector import containers, providers
from src import services

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

    document_service = providers.Factory(
        services.Document,
        base_path=config.provided.path_documents,
        document_repository=document_repository,
    )
    processed_image_service = providers.Factory(
        services.ProcessedImage,
        base_path=config.provided.path_images,
        document_repository=document_repository,
        processed_image_repository=processed_image_repository,
    )
    render_service = providers.Factory(
        services.Render,
        path_documents=config.provided.path_documents,
        path_images=config.provided.path_images,
        document_repository=document_repository,
        processed_image_repository=processed_image_repository,
    )
