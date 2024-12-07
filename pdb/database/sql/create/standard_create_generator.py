from pdb.database.datatypes.datatype_converter import DatatypeConverter
from pdb.database.datatypes.datatypes import PdbDatatype
from pdb.database.sql.create.create_generator import CreateGenerator
from typing import Any


class StandardCreateGenerator(CreateGenerator):
    def __init__(self, dtype_converter: DatatypeConverter) -> None:
        self._conv = dtype_converter

    def generate_create(self, table: str, columns: list[tuple[str, PdbDatatype, bool]]) -> tuple[str, list[Any]]:
        sql = f"CREATE TABLE IF NOT EXISTS {table} ("
        sql += ",".join([f"{c[0]} {self._conv.from_pdb_datatype(c[1]).value}" for c in columns])
        sql += ");"
        return (sql, [])
