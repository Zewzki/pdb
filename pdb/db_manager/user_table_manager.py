from typing import Any
from pdb.database.connectors.db_connector import DbConnector
from pdb.database.sql.sql_collection import SqlCollection
from pdb.shared.op_status import OpStatus
from pdb.database.common import OrderDir, SqlOp
from pdb.database.sql.conditions.condition import ConditionSet
from pdb.db_manager.constants import COL_ROWID


class UserTableManager:
    def __init__(self, db: DbConnector, sql: SqlCollection) -> None:
        self._db = db
        self._sql = sql

    def query(
        self,
        tablename: str,
        return_fields: list[str] | None = None,
        conditions: ConditionSet | None = None,
        order_by: str | None = None,
        order_dir: OrderDir = OrderDir.ASC,
        limit: int | None = None,
        offset: int | None = None,
        base_op: SqlOp = SqlOp.AND,
    ) -> OpStatus:
        sql, params = self._sql.query_generator.create_query(tablename, return_fields, conditions, order_by, order_dir, limit, offset, base_op)
        try:
            results = self._db.read(sql, params)
            return OpStatus(True, results)
        except Exception as ex:
            return OpStatus(False, f"Error running query - {ex}")

    def add_record(self, tablename: str, record_data: list[tuple[str, Any]]) -> OpStatus:
        sql, params = self._sql.insert_generator.generate_insert(tablename, record_data)
        try:
            self._db.write(sql, params)
            return OpStatus(True, f"Record added...")
        except Exception as ex:
            return OpStatus(False, f"Error adding record - {ex}")

    def update_record(self, tablename: str, row_id: int, puts: list[tuple[str, Any]]) -> OpStatus:
        sql, params = self._sql.update_generator.generate_update(tablename, puts, [(COL_ROWID, row_id)])

        try:
            self._db.write(sql, params)
            return OpStatus(True, f"Record updated...")
        except Exception as ex:
            return OpStatus(False, f"Error updating record - {ex}")

    def delete_record(self, tablename: str, row_id: int) -> OpStatus:
        sql, params = self._sql.delete_generator.generate_delete(tablename, ([COL_ROWID, row_id]))
        try:
            self._db.write(sql, params)
            return OpStatus(True, f"Record deleted...")
        except Exception as ex:
            return OpStatus(False, f"Error deleting record - {ex}")
