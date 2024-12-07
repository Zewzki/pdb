from abc import ABC, abstractmethod
from pdb.database.common import QueryPlaceholder
from typing import Any


class DbConnector(ABC):
    @abstractmethod
    def read(self, sql: str, params: list[Any] = None) -> list[Any]:
        pass

    @abstractmethod
    def write(self, sql: str, params: list[Any] = None):
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def query_placeholder(self) -> QueryPlaceholder:
        pass
