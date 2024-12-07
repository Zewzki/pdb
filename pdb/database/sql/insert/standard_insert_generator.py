from pdb.database.common import QueryPlaceholder
from pdb.database.sql.insert.insert_generator import InsertGenerator
from typing import Any


class StandardInsertGenerator(InsertGenerator):
    def __init__(self, query_placeholder: QueryPlaceholder) -> None:
        self._qp = query_placeholder.value

    def generate_insert(self, table: str, inserts: list[tuple[str, Any]]) -> tuple[str, list[Any]]:
        sql = f"INSERT INTO {table}"

        cols = [i[0] for i in inserts]
        params = [i[1] for i in inserts]

        col_str = "(" + ",".join(cols) + ")"
        val_str = "(" + ",".join([self._qp for i in inserts]) + ")"

        sql += f" {col_str} VALUES {val_str};"
        return (sql, params)
