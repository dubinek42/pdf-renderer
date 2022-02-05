from contextlib import contextmanager
from typing import Generator

import structlog
from pydantic import PostgresDsn
from sqlalchemy import create_engine, orm

log = structlog.get_logger(__name__)


class SessionFactory:
    def __init__(self, db_dsn: PostgresDsn) -> None:
        self._engine = create_engine(db_dsn)
        self._session_factory = orm.scoped_session(orm.sessionmaker(bind=self._engine))

    @contextmanager
    def open_session(self) -> Generator[orm.Session, None, None]:
        session: orm.Session = self._session_factory()
        try:
            yield session
        except Exception as exc:
            log.exception("database.open_session.failed", exc=exc)
            session.rollback()
            raise
        finally:
            session.close()
