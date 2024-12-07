from pdb.tools.importers.importer import Importer
from typing import Any


class CsvImporter(Importer):
    def create_import(self, path: str, delimiter: str = ",") -> tuple[list[str], list[list[Any]]]:
        content = None
        with open(path, "r") as f:
            content = f.read()

        if content is None or len(content) <= 0:
            return []

        lines = content.splitlines()
        cols = lines[0].split(delimiter)
        data = []
        for line in lines:
            record = []
            spl = line.split(delimiter)
            record.extend(spl[: len(cols) - 1])
            record.append("".join(spl[len(cols) :]))
            data.append(record)

        return (cols, data)
