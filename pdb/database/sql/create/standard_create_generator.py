from pdb.database.datatypes.datatype_converter import DatatypeConverter
from pdb.database.datatypes.datatypes import PdbDatatype
from pdb.database.sql.create.create_generator import CreateGenerator
from typing import Any
from pdb.database.models.pdb_column import PdbColumn


class StandardCreateGenerator(CreateGenerator):
    def __init__(self, dtype_converter: DatatypeConverter) -> None:
        self._conv = dtype_converter

    def generate_create(self, table: str, columns: list[PdbColumn]) -> tuple[str, list[Any]]:
        sql = f"CREATE TABLE IF NOT EXISTS {table} ("
        sql += ",".join([f"{c.col_name} {self._conv.from_pdb_datatype(c.dtype).value}" for c in columns])

        unique_cols = [c for c in columns if c.is_unique]
        if len(unique_cols) > 0:
            sql += f",UNIQUE({','.join([c.col_name for c in unique_cols])})"

        sql += ");"
        return (sql, [])
