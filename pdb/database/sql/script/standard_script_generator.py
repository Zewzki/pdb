from pdb.database.common import QueryPlaceholder
from pdb.database.sql.script.script_generator import ScriptGenerator
from typing import Any


class StandardScriptGenerator(ScriptGenerator):
    def __init__(self, query_placeholder: QueryPlaceholder) -> None:
        self._qp = query_placeholder

    def generate_script(self, statements: list[str], params_list: list[list[Any]]) -> str:
        sql = "BEGIN;\n"
        for statement, params in zip(statements, params_list, strict=True):
            processed = statement
            for param in params:
                processed = processed.replace(self._qp.value, f"'{str(param)}'", count=1)
            sql += f"{processed}\n"
        sql += "COMMIT;"
        return sql
