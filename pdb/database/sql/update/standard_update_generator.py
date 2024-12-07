from pdb.database.common import QueryPlaceholder
from pdb.database.sql.conditions.condition import ConditionSet
from pdb.database.sql.conditions.standard_condition_generator import StandardConditionGenerator
from pdb.database.sql.update.update_generator import UpdateGenerator
from typing import Any


class StandardUpdateGenerator(UpdateGenerator):
    def __init__(self, query_placeholder: QueryPlaceholder) -> None:
        self._qp = query_placeholder.value
        self._cg = StandardConditionGenerator(query_placeholder)

    def generate_update(
        self,
        table: str,
        puts: list[str, Any],
        conditions: ConditionSet | None = None,
    ) -> tuple[str, list[Any]]:
        sql = f"UPDATE {table} SET "
        params = [p[1] for p in puts]

        sql += ",".join([f"{p[0]}={self._qp}" for p in puts])

        if conditions:
            cond_str, cond_params = self._cg.generate_conditions(conditions)
            sql += f" {cond_str}"
            params.extend(cond_params)

        sql += ";"
        return (sql, params)
