import alembic
import pytest
from alembic.config import Config as AlembicConfig
from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from src.api.app import PdfRendererAPI

pytest_plugins = ["test.factories"]


class TestConfig(BaseSettings):
    db_dsn: str
    debug = False


@pytest.fixture
def client():
    app = PdfRendererAPI(TestConfig()).app.app
    return app.test_client()


@pytest.fixture(scope="function")
def db():
    test_config = TestConfig()
    assert "_test" == test_config.db_dsn[-5:]
    engine = create_engine(test_config.db_dsn)
    session_factory = sessionmaker(bind=engine)

    _db = {
        "engine": engine,
        "session_factory": session_factory,
    }

    alembic_config = AlembicConfig("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", test_config.db_dsn)
    alembic.command.upgrade(alembic_config, "head")

    yield _db

    alembic.command.downgrade(alembic_config, "base")
    engine.dispose()


@pytest.fixture(scope="function")
def open_session(db):
    session = scoped_session(db["session_factory"])
    yield session
    session.remove()
