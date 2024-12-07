from pdb.database.common import SQL_NULL, QueryPlaceholder, SqlOp
from pdb.database.sql.conditions.condition import Condition, ConditionGroup, ConditionSet, Evaluatable
from pdb.database.sql.conditions.condition_generator import ConditionGenerator
from typing import Any


class StandardConditionGenerator(ConditionGenerator):
    def __init__(self, query_placeholder: QueryPlaceholder) -> None:
        self._qp = query_placeholder.value

    def generate_conditions(self, conditions: ConditionSet, base_op: SqlOp = SqlOp.AND) -> tuple[str, list[Any]]:
        if len(conditions) <= 0:
            return ("", [])

        mapped_conds: list[Evaluatable] = []
        params = []

        for cond in conditions:
            col_name = cond[0]
            val = cond[1]
            op = SqlOp.EQ

            if len(cond) >= 3:
                op = cond[2]

            if val is None:
                mapped_conds.append(self._handle_null_val(col_name, op))

            mapped_conds.append(Condition(col_name, str(val), [op]))

        cg = ConditionGroup(mapped_conds, [base_op])
        sql, params = cg.eval()
        sql = sql[1:-1]
        sql = sql.format(QP=self._qp)

        return (f"WHERE {sql}", params)

    def _handle_null_val(self, col_name: str, op: SqlOp) -> Condition:
        if op == SqlOp.EQ or op is None:
            return Condition(col_name, SQL_NULL, [SqlOp.IS])
        if op == SqlOp.NE:
            return Condition(col_name, SQL_NULL, [SqlOp.IS, SqlOp.NOT])
        return Condition(col_name, SQL_NULL, [op])
