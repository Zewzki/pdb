from pdb.database.connectors.db_connector import DbConnector
from pdb.database.models.pdb_column import PdbColumn
from pdb.database.sql.sql_collection import SqlCollection
from pdb.db_manager.constants import (
    AUTH_COLUMNS,
    COL_COLNAME,
    COL_DATATYPE,
    COL_ISDROP,
    COL_ISUNIQUE,
    COL_TABLENAME,
    DROPDOWNS_COLUMNS,
    METADATA_COLUMNS,
    PERMS_COLUMNS,
    SESSION_COLUMNS,
    TABLE_AUTH,
    TABLE_DROPDOWNS,
    TABLE_METADATA,
    TABLE_PERMS,
    TABLE_SESS,
)
from pdb.shared.op_status import OpStatus
from typing import Any


class MetaTableManager:
    def __init__(self, db: DbConnector, sql_collection: SqlCollection) -> None:
        self._db = db
        self._sql = sql_collection

    def initialize_internal_tables(self) -> OpStatus:
        op = self._create_table(TABLE_METADATA, METADATA_COLUMNS)
        if not op.status:
            print(op.content)

        op = self._create_table(TABLE_DROPDOWNS, DROPDOWNS_COLUMNS)
        if not op.status:
            print(op.content)

        op = self._create_table(TABLE_AUTH, AUTH_COLUMNS)
        if not op.status:
            print(op.content)

        op = self._create_table(TABLE_SESS, SESSION_COLUMNS)
        if not op.status:
            print(op.content)

        op = self._create_table(TABLE_PERMS, PERMS_COLUMNS)
        if not op.status:
            print(op.content)

    def _initialize_metatable(self) -> OpStatus:
        op = self._create_table(TABLE_METADATA, METADATA_COLUMNS)
        if not op.status:
            print(op.content)

        sql_list: list[str] = []
        params_list: list[Any] = []

        for col in METADATA_COLUMNS:
            inserts = self._column_to_insert_list(TABLE_METADATA, col)
            sql, params = self._sql.insert_generator.generate_insert(TABLE_METADATA, inserts)
            sql_list.append(sql)
            params_list.append(params)

    def get_tables(self) -> OpStatus:
        sql = f"SELECT DISTINCT(tablename) FROM {TABLE_METADATA};"
        try:
            results = self._db.read(sql)
            if results is None or len(results) <= 0:
                return OpStatus(False, [])

            return OpStatus(True, [r[0] for r in results])
        except Exception as ex:
            return OpStatus(False, f"Error fetching user tables - {ex}")

    def add_table(self, tablename: str, columns: list[PdbColumn]) -> OpStatus:
        sql_list: list[str] = []
        params_list: list[list[Any]] = []

        sql1, params1 = self._sql.create_generator.generate_create(tablename, columns)
        sql_list.append(sql1)
        params_list.append(params1)

        for c in columns:
            inserts = self._column_to_insert_list(tablename, c)
            sql, params = self._sql.insert_generator.generate_insert(TABLE_METADATA, inserts)
            sql_list.append(sql)
            params_list.append(params)

        script = self._sql.script_generator.generate_script(sql_list, params_list)

        try:
            self._db.write_script(script)
            return OpStatus(True, f"Table {tablename} addedd...")
        except Exception as ex:
            return OpStatus(False, f"Error adding table {tablename} with columns {columns} - {ex}")

    def remove_table(self, tablename: str) -> OpStatus:
        sql1, params1 = self._sql.delete_generator.generate_delete(TABLE_METADATA, [(COL_TABLENAME, tablename)])
        sql2, params2 = self._sql.drop_generator.generate_drop(tablename)
        sql3, params3 = self._sql.delete_generator.generate_delete(TABLE_DROPDOWNS, [(COL_TABLENAME, tablename)])
        sql4, params4 = self._sql.delete_generator.generate_delete(TABLE_PERMS, [(COL_TABLENAME, tablename)])
        script = self._sql.script_generator.generate_script([sql1, sql2, sql3, sql4], [params1, params2, params3, params4])
        try:
            self._db.write_script(script)
            return OpStatus(True, f"Table {tablename} removed...")
        except Exception as ex:
            return OpStatus(False, f"Error removing table {tablename} - {ex}")

    def rename_table(self, old_tablename: str, new_tablename: str) -> OpStatus:
        sql1, params1 = self._sql.alter_generator.generate_rename_table(old_tablename, new_tablename)
        sql2, params2 = self._sql.update_generator.generate_update(TABLE_METADATA, [(COL_TABLENAME, new_tablename)], [(COL_TABLENAME, old_tablename)])
        sql3, params3 = self._sql.update_generator.generate_update(TABLE_DROPDOWNS, [(COL_TABLENAME, new_tablename)], [(COL_TABLENAME, old_tablename)])
        sql4, params4 = self._sql.update_generator.generate_update(TABLE_PERMS, [(COL_TABLENAME, new_tablename)], [(COL_TABLENAME, old_tablename)])
        script = self._sql.script_generator.generate_script([sql1, sql2, sql3, sql4], [params1, params2, params3, params4])

        try:
            self._db.write_script(script)
            return OpStatus(True, f"Renamed table {old_tablename} to {new_tablename}")
        except Exception as ex:
            return OpStatus(False, f"Error renaming table {old_tablename} to {new_tablename} - {ex}")

    def add_table_column(self, tablename: str, column: PdbColumn) -> OpStatus:
        sql1, params1 = self._sql.insert_generator.generate_insert(
            TABLE_METADATA,
            [
                (COL_TABLENAME, tablename),
                (COL_COLNAME, column.col_name),
                (COL_DATATYPE, self._sql.dtype_converter.from_pdb_datatype(column.dtype).value),
                (COL_ISDROP, column.is_dropdown),
                (COL_ISUNIQUE, column.is_unique),
            ],
        )
        sql2, params2 = self._sql.alter_generator.generate_add_column(tablename, column.col_name, column.dtype.value)
        script = self._sql.script_generator.generate_script([sql1, sql2], [params1, params2])

        try:
            self._db.write_script(script)
            return OpStatus(True, f"Added column {column.col_name} ({column.dtype.name}) to table {tablename}")
        except Exception as ex:
            return OpStatus(False, f"Error adding column {column.col_name} ({column.dtype.name}) to table {tablename}")

    def rename_column(self, tablename: str, old_column_name: str, new_column_name: str) -> OpStatus:
        sql1, params1 = self._sql.update_generator.generate_update(
            TABLE_METADATA,
            puts=[(COL_COLNAME, new_column_name)],
            conditions=[(COL_TABLENAME, tablename), (COL_COLNAME, old_column_name)],
        )
        sql2, params2 = self._sql.alter_generator.generate_rename_column(tablename, old_column_name, new_column_name)
        sql3, params3 = self._sql.update_generator.generate_update(
            TABLE_DROPDOWNS,
            [(COL_COLNAME, new_column_name)],
            [(COL_TABLENAME, tablename), (COL_COLNAME, old_column_name)],
        )
        script = self._sql.script_generator.generate_script([sql1, sql2, sql3], [params1, params2, params3])

        try:
            self._db.write_script(script)
            return OpStatus(True, f"Renamed column {old_column_name} to {new_column_name} on table {tablename}")
        except Exception as ex:
            return OpStatus(False, f"Error renaming column {old_column_name} to {new_column_name} on table {tablename}")

    def remove_table_column(self, tablename: str, column_name: str) -> OpStatus:
        sql1, params1 = self._sql.delete_generator.generate_delete(TABLE_METADATA, [(COL_TABLENAME, tablename), (COL_COLNAME, column_name)])
        sql2, params2 = self._sql.alter_generator.generate_drop_column(tablename, column_name)
        sql3, params3 = self._sql.delete_generator.generate_delete(TABLE_DROPDOWNS, [(COL_TABLENAME, tablename), (COL_COLNAME, column_name)])
        script = self._sql.script_generator.generate_script([sql1, sql2, sql3], [params1, params2, params3])

        try:
            self._db.write_script(script)
            return OpStatus(True, f"PdbColumn {column_name} removed from table {tablename}")
        except Exception as ex:
            return OpStatus(False, f"Error removing column {column_name} from table {tablename} - {ex}")

    def _create_table(self, tablename: str, columns: list[PdbColumn]) -> OpStatus:
        sql, params = self._sql.create_generator.generate_create(tablename, columns)
        try:
            self._db.write(sql, params)
        except Exception as ex:
            return OpStatus(False, f"Error creating table {tablename} with columns {columns} - {ex}")
        return OpStatus(True, f"Table {tablename} created...")

    def _column_to_insert_list(self, tablename: str, column: PdbColumn) -> list[tuple, str]:
        return [
            (COL_TABLENAME, tablename),
            (COL_COLNAME, column.col_name),
            (COL_DATATYPE, self._sql.dtype_converter.from_pdb_datatype(column.dtype).value),
            (COL_ISDROP, column.is_dropdown),
            (COL_ISUNIQUE, column.is_unique),
        ]
