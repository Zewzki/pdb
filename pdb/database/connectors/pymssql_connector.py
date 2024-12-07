from pdb.database.common import QueryPlaceholder
from pdb.database.config.db_config import DbConfig
from pdb.database.connectors.db_connector import DbConnector
from typing import Any


class PymssqlConnector(DbConnector):
    def __init__(self, db_config: DbConfig) -> None:
        self._db_config = db_config
        self._debug = db_config.debug

    def query_placeholder(self) -> QueryPlaceholder:
        return QueryPlaceholder.PCENT

    def read(self, sql: str, params: list[Any] = None) -> list[Any]:
        return super().read(sql, params)

    def write(self, sql: str, params: list[Any] = None):
        return super().write(sql, params)

    def commit(self) -> None:
        return super().commit()

    def rollback(self) -> None:
        return super().rollback()

    def close(self) -> None:
        return super().close()
