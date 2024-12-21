from dataclasses import dataclass
from pdb.database.models.pdb_column import PdbColumn


@dataclass
class PdbTable:
    tablename: str
    unique_entries: bool
    columns: list[PdbColumn]
