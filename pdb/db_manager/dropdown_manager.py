from pdb.database.connectors.db_connector import DbConnector
from pdb.database.sql.sql_collection import SqlCollection
from pdb.shared.op_status import OpStatus
from pdb.db_manager.constants import TABLE_DROPDOWNS, COL_TABLENAME, COL_COLNAME, COL_VAL
from typing import Any


class DropdownManager:
    def __init__(self, db: DbConnector, sql: SqlCollection) -> None:
        self._db = db
        self._sql = sql

    def get_dropdowns(self, tablename: str, column_name: str) -> OpStatus:
        sql, params = self._sql.query_generator.create_query(
            TABLE_DROPDOWNS,
            return_fields=[COL_TABLENAME, COL_COLNAME, COL_VAL],
            conditions=[(COL_TABLENAME, tablename), (COL_COLNAME, column_name)],
        )

        try:
            results = self._db.write(sql, params)
            if results is None or len(results) <= 0:
                return OpStatus(True, [])

            return OpStatus(True, [r[2] for r in results])
        except Exception as ex:
            return OpStatus(False, f"Error fetching dropdowns - {ex}")

    def add_dropdown_value(self, tablename: str, column_name: str, value: Any) -> OpStatus:
        sql, params = self._sql.insert_generator.generate_insert(TABLE_DROPDOWNS, [(COL_TABLENAME, tablename), (COL_COLNAME, column_name), (COL_VAL, value)])

        try:
            self._db.write(sql, params)
            return OpStatus(True, f"Addedd dropdown value {value} for table {tablename}, column {column_name}...")
        except Exception as ex:
            return OpStatus(False, f"Error adding dropdown value {value} for table {tablename}, column {column_name} - {ex}")

    def remove_dropdown_value(self, tablename: str, column_name: str, value: Any) -> OpStatus:
        sql, params = self._sql.delete_generator.generate_delete(TABLE_DROPDOWNS, [(COL_TABLENAME, tablename), (COL_COLNAME, column_name), (COL_VAL, value)])

        try:
            self._db.write(sql, params)
            return OpStatus(True, f"Removed dropdown value {value} for table {tablename}, column {column_name}...")
        except Exception as ex:
            return OpStatus(False, f"Error removing dropdown value {value} for table {tablename}, column {column_name} - {ex}")
