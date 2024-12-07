from pathlib import Path

class PdbConfig:

    def __init__(self, path: Path) -> None:
        self._path = path
        self.pdbs: list[str] = []

    def load(self):
        pass

    def save(self):
        pass