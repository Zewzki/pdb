from pdb.database.common import QueryPlaceholder
from pdb.database.sql.conditions.condition import ConditionSet
from pdb.database.sql.conditions.standard_condition_generator import StandardConditionGenerator
from pdb.database.sql.delete.delete_generator import DeleteGenerator
from typing import Any


class StandardDeleteGenerator(DeleteGenerator):
    def __init__(self, query_placeholder: QueryPlaceholder) -> None:
        self._qp = query_placeholder.value
        self._cg = StandardConditionGenerator(query_placeholder)

    def generate_delete(self, table: str, conditions: ConditionSet | None = None) -> tuple[str, list[Any]]:
        sql = f"DELETE FROM {table}"
        params = []

        if conditions:
            cond_str, cond_params = self._cg.generate_conditions(conditions)
            sql += f" {cond_str}"
            params.extend(cond_params)

        sql += ";"
        return (sql, params)
