from contextlib import contextmanager
from typing import Generator

import sqlalchemy
import structlog
from pydantic import PostgresDsn
from sqlalchemy import create_engine, orm

log = structlog.get_logger(__name__)


class SessionNotOpenError(Exception):
    pass


class SessionFactory:
    def __init__(self, db_dsn: PostgresDsn) -> None:
        self._engine = create_engine(db_dsn)
        self._session_factory = orm.scoped_session(orm.sessionmaker(bind=self._engine))

    @contextmanager
    def open_session(self) -> Generator[orm.Session, None, None]:
        session: orm.Session = self._session_factory()
        try:
            yield session
        except sqlalchemy.exc.OperationalError as exc:
            log.exception("database.open_session.failed", exc=exc)
            session.rollback()
            raise SessionNotOpenError
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
