from pdb.database.common import QueryPlaceholder
from pdb.database.config.db_config import DbConfig
from pdb.database.connectors.db_connector import DbConnector
from typing import Any

import psycopg2 as pg


class Psycopg2Connector(DbConnector):
    def __init__(self, db_config: DbConfig) -> None:
        self._config = db_config
        parsed_opts = (
            "-c " + " ".join([f"{k}={v}" for k, v in db_config.options.items()])
            if db_config.options is not None
            else ""
        )
        self.cnx = pg.connect(
            user=self._config.user,
            password=self._config.password,
            host=self._config.host,
            port=int(self._config.port),
            dbname=self._config.db,
            options=parsed_opts,
        )
        self.debug = self._config.debug

    def read(self, sql: str, params: list[Any] = None) -> list[Any]:
        try:
            cursor = self.cnx.cursor()
            if self.debug:
                print(f"{sql} - {params}")
            cursor.execute(sql, params)
            return cursor.fetchall()
        except Exception as e:
            self.cnx.rollback()
            raise e
        finally:
            cursor.close()

    def write(self, sql: str, params: list[Any] = None):
        try:
            cursor = self.cnx.cursor()
            if self.debug:
                print(f"{sql} - {params}")
            cursor.execute(sql, params)
            self.cnx.commit()
        except Exception as e:
            if cursor is not None:
                self.cnx.rollback()
            raise e
        finally:
            if cursor is not None:
                cursor.close()

    def commit(self) -> None:
        self.cnx.commit()

    def rollback(self) -> None:
        self.cnx.rollback()

    def close(self) -> None:
        self.cnx.close()

    def query_placeholder(self) -> QueryPlaceholder:
        return QueryPlaceholder.PCENT
