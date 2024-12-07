from pdb.database.common import SupportedDb
from pdb.database.config.db_config import DbConfig
from pdb.database.connectors.connector_factory import ConnectorFactory
from pdb.database.datatypes.datatype_converter_factory import DatatypeConverterFactory
from pdb.database.datatypes.datatypes import PdbDatatype
from pdb.database.sql.sql_collection import SqlCollection
from pdb.database.sql.sql_factory import SqlFactory
from pdb.db_manager.db_manager import DbManager
from pdb.shared.hash.algorithms import Sha256
from pdb.shared.salt.random_salter import RandomSalter
from pdb.tools.exporters.csv_exporter import CsvExporter
from pdb.tools.importers.csv_importer import CsvImporter


class ImportExportTester:
    def __init__(self) -> None:
        hasher = Sha256()
        salter = RandomSalter()
        dbtype = SupportedDb.SQLITE3
        db_config = DbConfig(host="/home/zewzki/Projects/pdb/pdb/tests/db/listening.sqlite3", debug=True)
        db = ConnectorFactory.create_connector(dbtype, db_config)
        sql = SqlCollection(
            DatatypeConverterFactory.create_datatype_converter(dbtype),
            SqlFactory.create_create_generator(dbtype),
            SqlFactory.create_query_generator(dbtype),
            SqlFactory.create_insert_generator(dbtype),
            SqlFactory.create_update_generator(dbtype),
            SqlFactory.create_delete_generator(dbtype),
            SqlFactory.create_drop_generator(dbtype),
            SqlFactory.create_alter_generator(dbtype),
        )
        self._man = DbManager(db, sql, hasher, salter)
        self._test_cols: list[tuple[str, PdbDatatype, bool]] = [
            ("ReleaseDate", PdbDatatype.DATE, False),
            ("Band", PdbDatatype.TEXT, False),
            ("Type", PdbDatatype.TEXT, True),
            ("Album", PdbDatatype.TEXT, False),
            ("Style", PdbDatatype.TEXT, False),
            ("Rating", PdbDatatype.DECIMAL, False),
            ("Comments", PdbDatatype.TEXT, False),
        ]

        self._csv_importer = CsvImporter()
        self._csv_exporter = CsvExporter()

        self._man.initialize_metatables()
        self._man.create_pdb_table("listening_2024", self._test_cols)

    def test_import(self) -> None:
        cols, data = self._csv_importer.create_import("./pdb/tests/db/musicData.csv")
        for row in data:
            try:
                s = self._man.add_record("listening_2024", [(x[0], x[1]) for x in zip(cols, row, strict=True)])
                if not s.status:
                    print(s.msg)
            except ValueError as e:
                print(f"Malformed CSV row, expected {len(cols)} columns {cols} but received {len(row)}: {row}")
