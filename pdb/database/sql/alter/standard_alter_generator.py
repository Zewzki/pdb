from pdb.database.datatypes.datatype_converter import DatatypeConverter
from pdb.database.datatypes.datatypes import PdbDatatype
from pdb.database.sql.alter.alter_generator import AlterGenerator
from typing import Any


class StandardAlterGenerator(AlterGenerator):
    def __init__(self, dtype_converter: DatatypeConverter) -> None:
        self._conv = dtype_converter

    def generate_rename_table(self, old_tablename: str, new_tablename: str) -> tuple[str, list[Any]]:
        sql = f"ALTER TABLE {old_tablename} RENAME TO {new_tablename};"
        return (sql, [])

    def generate_add_column(self, tablename: str, new_col_name: str, dtype: PdbDatatype) -> tuple[str, list[Any]]:
        sql = f"ALTER TABLE {tablename} ADD COLUMN {new_col_name} {self._conv.from_pdb_datatype(dtype)};"
        return (sql, [])

    def generate_drop_column(self, tablename: str, col_name: str) -> tuple[str, list[Any]]:
        sql = f"ALTER TABLE {tablename} DROP COLUMN {col_name};"
        return (sql, [])

    def generate_rename_column(self, tablename: str, old_col_name: str, new_col_name: str) -> tuple[str, list[Any]]:
        sql = f"ALTER TABLE {tablename} RENAME COLUMN {old_col_name} TO {new_col_name};"
        return (sql, [])
