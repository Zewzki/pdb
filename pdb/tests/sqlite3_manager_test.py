from pdb.database.common import SupportedDb
from pdb.database.config.db_config import DbConfig
from pdb.database.connectors.connector_factory import ConnectorFactory
from pdb.database.datatypes.datatype_converter_factory import DatatypeConverterFactory
from pdb.database.datatypes.datatypes import PdbDatatype
from pdb.database.sql.sql_collection import SqlCollection
from pdb.database.sql.sql_factory import SqlFactory
from pdb.db_manager.db_manager import DbManager
from pdb.shared.hash.algorithms import Sha256
from pdb.shared.op_status import OpStatus
from pdb.shared.salt.random_salter import RandomSalter
from typing import Any


class Sqlite3ManagerTester:
    def __init__(self) -> None:
        hasher = Sha256()
        salter = RandomSalter()
        dbtype = SupportedDb.SQLITE3
        db_config = DbConfig(host="./pdb/tests/db/pdb.sqlite3", debug=True)
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
            ("name", PdbDatatype.TEXT, False),
            ("age", PdbDatatype.NUMBER, False),
            ("salary", PdbDatatype.DECIMAL, False),
            ("title", PdbDatatype.TEXT, True),
        ]

        self._man.initialize_metatables()

    def test_create(self) -> None:
        self._man.create_pdb_table("test_table", self._test_cols)

    def test_insert(self) -> None:
        # Add Users
        self._man.add_user("zewzki", "strongpassword", "admin")

        # Add perms
        self._man.add_user_permissions("test_table", "zewzki", True, True)

        # Add dropdowns
        self._man.add_dropdown_value("test_table", "title", "Junior Shrimp-eater")
        self._man.add_dropdown_value("test_table", "title", "Qualified Shrimp-eater")
        self._man.add_dropdown_value("test_table", "title", "Senior Shrimp-eater")
        self._man.add_dropdown_value("test_table", "title", "President Shrimp-eater")

        # Add data
        s = self._man.add_record(
            "test_table",
            [
                ("name", "shrimpbob joepants"),
                ("age", 16),
                ("salary", 65_000.45),
                ("title", "Junior Shrimp-eater"),
            ],
        )
        if not s.status:
            print(s.msg)

        s = self._man.add_record(
            "test_table",
            [
                ("name", "shrimpgus"),
                ("age", 33),
                ("salary", 55_400_000),
                ("title", "Senior Shrimp-eater"),
            ],
        )
        if not s.status:
            print(s.msg)

        s = self._man.add_record(
            "test_table",
            [
                ("name", "john shrimp"),
                ("age", 3),
                ("salary", 1.0),
                ("title", "President Shrimp-eater"),
            ],
        )
        if not s.status:
            print(s.msg)

    def test_select(self) -> list[list[Any]] | OpStatus:
        return self._man.get_table("test_table")
