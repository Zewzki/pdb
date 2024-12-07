from abc import ABC, abstractmethod
from pdb.database.common import OrderDir, SqlOp
from pdb.database.sql.conditions.condition import ConditionSet
from typing import Any


class QueryGenerator(ABC):
    @abstractmethod
    def create_query(
        self,
        table: str,
        return_fields: list[str] | None = None,
        conditions: ConditionSet | None = None,
        order_by: str | None = None,
        order_dir: OrderDir = OrderDir.DESC,
        limit: int | None = None,
        offset: int | None = None,
        base_op: SqlOp = SqlOp.AND,
    ) -> tuple[str, list[Any]]:
        pass
