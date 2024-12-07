from pdb.database.sql.drop.drop_generator import DropGenerator
from typing import Any


class StandardDropGenerator(DropGenerator):
    def __init__(self) -> None:
        pass

    def generate_drop(self, table: str) -> tuple[str, list[Any]]:
        return (f"DROP TABLE {table};", [])
