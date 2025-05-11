from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar, List

from sqlalchemy import ColumnElement

from app.db.base import SessionProvider
from app.models.base import ListResult

T = TypeVar("T")



@dataclass
class Query:
    filters: List[ColumnElement] = None
    sort: List[ColumnElement] = None

class BaseService(ABC, Generic[T]):
    def __init__(self, session_provider: SessionProvider):
        self.session_provider = session_provider

    @property
    def session(self):
        return self.session_provider.get_current_session()

    @abstractmethod
    async def get(self, id: int) -> T | None:
        pass

    @abstractmethod
    async def list(self, page: int, size: int) -> ListResult[T]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass
