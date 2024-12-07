from os import PathLike
from pathlib import Path
from pdb.database.config.db_config import DbConfig
from pdb.database.connectors.sqlite3_connector import Sqlite3Connector
from pdb.database.datatypes.datatypes import PdbDatatype
from pdb.database.datatypes.sqlite3_datatype_converter import Sqlite3DatatypeConverter
from pdb.db_manager.db_manager import DbManager
from pdb.shared.constants import SALT_LEN
from pdb.shared.hash.hash_algorithm import HashAlgorithm
from pdb.shared.op_status import OpStatus
from pdb.shared.salt.salter import Salter
from typing import Any, ClassVar


class Sqlite3Manager(DbManager):
    _DB_FILENAME: ClassVar[str] = "pdb.sqlite3"
    _PDB_TABLENAME: ClassVar[str] = "pdb"

    _METADATA_TABLENAME: ClassVar[str] = "table_metadata"
    _METADATA_COLUMNS: ClassVar[list[tuple[str, PdbDatatype]]] = [
        ("tablename", PdbDatatype.TEXT),
        ("col_name", PdbDatatype.TEXT),
        ("datatype", PdbDatatype.TEXT),
        ("is_dropdown", PdbDatatype.BOOL),
    ]

    _DROPDOWNS_TABLENAME: ClassVar[str] = "dropdowns"
    _DROPDOWNS_COLUMNS: ClassVar[list[tuple[str, PdbDatatype]]] = [
        ("tablename", PdbDatatype.TEXT),
        ("col_name", PdbDatatype.TEXT),
        ("value", PdbDatatype.TEXT),
    ]

    _AUTH_TABLENAME: ClassVar[str] = "auth"
    _AUTH_COLUMNS: ClassVar[list[tuple[str, PdbDatatype]]] = [
        ("username", PdbDatatype.TEXT),
        ("role", PdbDatatype.TEXT),
        ("pw_salt", PdbDatatype.TEXT),
        ("pw_hash", PdbDatatype.RAW),
        ("pw_algo", PdbDatatype.TEXT),
    ]

    _PERMS_TABLENAME: ClassVar[str] = "table_permissions"
    _PERMS_COLUMNS: ClassVar[list[tuple[str, PdbDatatype]]] = [
        ("tablename", PdbDatatype.TEXT),
        ("username", PdbDatatype.TEXT),
        ("can_read", PdbDatatype.BOOL),
        ("can_write", PdbDatatype.BOOL),
    ]

    def __init__(self, save_dir: PathLike, hasher: HashAlgorithm, salter: Salter, debug: bool) -> None:
        self._save_dir = save_dir
        self._debug = debug
        self._table_path = Path(self._save_dir) / self._DB_FILENAME
        self._config = DbConfig(host=Path(self._save_dir) / self._DB_FILENAME, debug=debug)
        self._cnxer = Sqlite3Connector(self._config)
        self._dtype_conv = Sqlite3DatatypeConverter()
        self._hasher = hasher
        self._salter = salter
        self._create_table(self._METADATA_TABLENAME, self._METADATA_COLUMNS)
        self._create_table(self._DROPDOWNS_TABLENAME, self._DROPDOWNS_COLUMNS)
        self._create_table(self._AUTH_TABLENAME, self._AUTH_COLUMNS)
        self._create_table(self._PERMS_TABLENAME, self._PERMS_COLUMNS)

    # Tables
    def create_pdb_table(self, tablename: str, columns: list[tuple[str, PdbDatatype, bool]]) -> OpStatus:
        metatable_sql = f"INSERT INTO {self._METADATA_TABLENAME} (tablename, col_name, datatype, is_dropdown) VALUES "
        metatable_sql += ",".join(["(?,?,?,?)" for _ in columns])
        metatable_sql += ";"
        metatable_params = []
        for c in columns:
            metatable_params.append(tablename)
            metatable_params.append(c[0])
            metatable_params.append(c[1].value)
            metatable_params.append(c[2])
        self._cnxer.write(metatable_sql, metatable_params)

        self._create_table(tablename, columns)

    def _create_table(self, tablename: str, columns: list[tuple[str, PdbDatatype, bool]]) -> OpStatus:
        sql = f"CREATE TABLE IF NOT EXISTS {tablename} ("
        sql += ",".join([f"{c[0]} {self._dtype_conv.from_pdb_datatype(c[1]).value}" for c in columns])
        sql += ");"
        self._cnxer.write(sql)

    def get_pdb_tables(self) -> list[str]:
        sql = f"SELECT DISTINCT tablename FROM {self._METADATA_TABLENAME};"
        return self._cnxer.read(sql)

    def remove_pdb_table(self, tablename: str) -> OpStatus:
        self.remove_record_by_values(self._METADATA_TABLENAME, [("tablename", tablename)])
        self._remove_table(tablename)

    def _remove_table(self, tablename: str) -> OpStatus:
        sql = f"DROP TABLE {tablename};"
        self._cnxer.write(sql)

    # Table Columns
    def add_table_column(self, tablename: str, column_name: str, type: type) -> OpStatus:
        pass

    def modify_table_column(self, tablename: str, column_name: str, new_type: type) -> OpStatus:
        pass

    def remove_table_column(self, tablename: str, column_name: str) -> OpStatus:
        pass

    # Dropdowns
    def add_dropdown_value(self, tablename: str, column_name: str, value: Any) -> OpStatus:
        self.add_record(
            self._DROPDOWNS_TABLENAME,
            {
                "tablename": tablename,
                "col_name": column_name,
                "value": value,
            },
        )

    def remove_dropdown_value(self, tablename: str, column_name: str, value: Any) -> OpStatus:
        self.remove_record_by_values(
            self._DROPDOWNS_TABLENAME,
            {
                "tablename": tablename,
                "col_name": column_name,
                "value": value,
            },
        )

    # Users
    def add_user(self, username: str, password: str, role: str) -> OpStatus:
        pw_salt = self._salter.generate_salt(SALT_LEN)
        pw_hash = self._hasher.hash(password, pw_salt)
        self.add_record(
            self._AUTH_TABLENAME,
            {
                "username": username,
                "role": role,
                "pw_hash": pw_hash,
                "pw_salt": pw_salt,
                "pw_algo": self._hasher.name,
            },
        )

    def remove_user(self, username: str) -> OpStatus:
        self.remove_record_by_values(self._AUTH_TABLENAME, conditions=[("username", username)])

    # Perms
    def add_user_permissions(self, tablename: str, username: str, can_read: bool, can_write: bool) -> OpStatus:
        self.add_record(
            self._PERMS_TABLENAME,
            record_data={
                "tablename": tablename,
                "username": username,
                "can_read": can_read,
                "can_write": can_write,
            },
        )

    # Table Data
    def get_table(self, tablename: str) -> list[list[Any]] | OpStatus:
        sql = f"SELECT * FROM {tablename};"
        return self._cnxer.read(sql)

    def add_record(self, tablename: str, record_data: dict[str, Any]) -> OpStatus:
        keys = list(record_data.keys())
        sql = f"INSERT INTO {tablename} "
        sql += "(" + ",".join([str(key) for key in keys]) + ") "
        sql += "VALUES (" + ",".join(["?" for _ in keys]) + ");"
        params = [record_data[key] for key in keys]
        return self._cnxer.write(sql, params)

    def update_record(self, tablename: str, row_id: int, new_data: dict[str, Any]) -> OpStatus:
        pass

    def remove_record(self, tablename: str, row_id: int) -> OpStatus:
        sql = f"DELETE FROM {tablename} WHERE ROWID=?;"
        return self._cnxer.write(sql, [row_id])

    def remove_record_by_values(self, tablename: str, conditions: list[tuple[str, Any]]) -> OpStatus:
        sql = f"DELETE FROM {tablename} WHERE "
        sql += " AND ".join([f"{c[0]}=?" for c in conditions])
        sql += ";"
        params = [c[1] for c in conditions]

        return self._cnxer.write(sql, params)
