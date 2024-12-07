from abc import ABC, abstractmethod
from pdb.database.common import SQL_NULL, SqlOp
from typing import Any

ConditionSet = list[tuple[str, Any] | tuple[str, Any, SqlOp]]


class Evaluatable(ABC):
    @abstractmethod
    def eval(self) -> tuple[str, list[Any]]:
        pass


class Condition(Evaluatable):
    def __init__(self, col_name: str, val: Any, ops: list[SqlOp] = [SqlOp.EQ]) -> None:
        self._col_name = col_name
        self._val = str(val)
        self._ops = ops

    def eval(self) -> tuple[str, list[Any]]:
        op_list = " ".join([o.value for o in self._ops])
        if self._val == SQL_NULL:
            return (f"{self._col_name} {op_list} {self._val}", [])

        sql = f"{self._col_name} {op_list} " + "{QP}"
        return (sql, [self._val])


class ConditionGroup(Evaluatable):
    def __init__(self, conditions: list[Evaluatable], ops: list[SqlOp] = [SqlOp.AND]) -> None:
        self._conditions = conditions
        self._ops = ops

    def eval(self) -> tuple[str, list[Any]]:
        op_str = " ".join([o.value for o in self._ops])

        evals = []
        params = []

        for c in self._conditions:
            e, p = c.eval()
            evals.append(e)
            params.extend(p)

        s = "(" + f" {op_str} ".join(evals) + ")"
        return (s, params)
