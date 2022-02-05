from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session


class Repository:
    def __init__(
        self, open_session: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self._open_session = open_session
