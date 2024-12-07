from pdb.database.common import OrderDir, QueryPlaceholder, SqlOp
from pdb.database.sql.conditions.condition import ConditionSet
from pdb.database.sql.conditions.standard_condition_generator import StandardConditionGenerator
from pdb.database.sql.query.query_generator import QueryGenerator
from typing import Any


class Sqlite3QueryGenerator(QueryGenerator):
    def __init__(self, query_placeholder: QueryPlaceholder) -> None:
        self._qp = query_placeholder
        self._cg = StandardConditionGenerator(query_placeholder)

    def create_query(
        self,
        table: str,
        return_fields: list[str] | None = None,
        conditions: ConditionSet | None = None,
        order_by: str | None = None,
        order_dir: OrderDir | None = OrderDir.DESC,
        limit: int | None = None,
        offset: int | None = None,
        base_op: SqlOp | None = SqlOp.AND,
    ) -> tuple[str, list[Any]]:
        params = []
        sql = "SELECT "

        if return_fields is None:
            sql += "*"
        else:
            sql += ",".join(return_fields)

        sql += f" FROM {table}"

        if conditions:
            condition_str, condition_params = self._cg.generate_conditions(conditions)
            sql += f" {condition_str}"
            params.extend(condition_params)

        if order_by is not None:
            sql += f" ORDER BY {order_by} {order_dir.value}"

        if limit is not None:
            sql += f" LIMIT {int(limit)}"

        if offset is not None:
            sql += f" OFFSET {int(offset)}"

        sql += ";"
        return (sql, params)
