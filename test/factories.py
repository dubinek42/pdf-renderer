import pytest
from factory.alchemy import SQLAlchemyModelFactory
from factory.declarations import Sequence
from src import services
from src.db import models, repositories
from src.models import ProcessingStatus


@pytest.fixture(scope="function")
def document_factory(open_session):
    class DocumentFactory(SQLAlchemyModelFactory):
        id = Sequence(lambda n: n + 1)
        processing_status = ProcessingStatus.NEW
        pages_count = 1
        file_path = Sequence(lambda n: f"document{n + 1}.pdf")

        class Meta:
            model = models.Document
            sqlalchemy_session = open_session
            sqlalchemy_session_persistence = "commit"

    return DocumentFactory


@pytest.fixture()
def document_repository(open_session):
    return repositories.Document(open_session)


@pytest.fixture()
def document_service(document_repository):
    return services.Document("test", document_repository)
