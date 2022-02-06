from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from ..models import EntityName


class EntityNotFoundError(Exception):
    def __init__(self, entity_id: str, entity_name: EntityName) -> None:
        self.entity_id = entity_id
        self.entity_name = entity_name


class Repository:
    def __init__(
        self, open_session: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self._open_session = open_session
