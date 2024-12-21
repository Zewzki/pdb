import sqlite3
from pdb.database.common import QueryPlaceholder
from pdb.database.config.db_config import DbConfig
from pdb.database.connectors.db_connector import DbConnector
from typing import Any, ClassVar


class Sqlite3Connector(DbConnector):
    PLACEHOLDER: ClassVar[QueryPlaceholder] = QueryPlaceholder.QMARK

    def __init__(self, db_config: DbConfig) -> None:
        self._db_config = db_config
        self.debug = db_config.debug
        self._cnx = sqlite3.connect(self._db_config.host)

    def query_placeholder(self) -> QueryPlaceholder:
        return Sqlite3Connector.PLACEHOLDER

    def read(self, sql: str, params: tuple[Any] | None = None) -> list[tuple]:
        try:
            if params is None:
                params = ()
            cursor = self._cnx.cursor()
            if self.debug:
                print(f"{sql} - {params}")
            cursor.execute(sql, params)
            return cursor.fetchall()
        except Exception as e:
            self._cnx.rollback()
            raise e
        finally:
            cursor.close()

    def write(self, sql: str, params: tuple[Any] | None = None) -> None:
        try:
            if params is None:
                params = ()
            cursor = self._cnx.cursor()
            if self.debug:
                print(f"{sql} - {params}")
            cursor.execute(sql, params)
            self._cnx.commit()
        except Exception as e:
            if cursor is not None:
                self._cnx.rollback()
            raise e
        finally:
            if cursor is not None:
                cursor.close()

    def batch_write(self, sql: str, params: list[list[Any]]):
        try:
            cursor = self._cnx.cursor()
            if self.debug:
                print(f"{sql} - {params}")
            cursor.executemany(sql, params)
            self._cnx.commit()
        except Exception as e:
            if cursor is not None:
                self._cnx.rollback()
                raise e
        finally:
            if cursor is not None:
                cursor.close()

    def write_script(self, script):
        try:
            cursor = self._cnx.cursor()
            if self.debug:
                print(script)
            cursor.executescript(script)
            self._cnx.commit()
        except Exception as e:
            if cursor is not None:
                self._cnx.rollback()
                raise e
        finally:
            if cursor is not None:
                cursor.close()

    def commit(self) -> None:
        self._cnx.commit()

    def rollback(self) -> None:
        self._cnx.rollback()

    def close(self) -> None:
        self._cnx.close()
