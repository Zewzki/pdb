from pdb.shared.op_status import OpStatus
from pdb.tools.exporters.exporter import Exporter
from typing import Any


class CsvExporter(Exporter):
    def export(self, col_names: list[str], data: list[list[Any]], output_path: str) -> OpStatus:
        write_str = ",".join(col_names) + "\n"
        write_str += "\n".join([",".join(row) for row in data])

        with open(output_path, "w") as f:
            f.write(write_str)
