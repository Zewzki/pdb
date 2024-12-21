from pdb.database.connectors.db_connector import DbConnector
from pdb.database.sql.sql_collection import SqlCollection

from pdb.shared.hash.hash_algorithm import HashAlgorithm
from pdb.shared.op_status import OpStatus
from pdb.shared.salt.salter import Salter
from pdb.shared.hash.hasher_factory import HasherFactory
from pdb.shared.salt.salt_factory import SaltFactory
from pdb.shared.hash.supported_hash import SupportedHash
from pdb.shared.salt.supported_salter import SupportedSalter
from pdb.db_manager.constants import (
    TABLE_AUTH,
    COL_PW_ALGO,
    COL_PW_HASH,
    COL_PW_SALT,
    COL_ROLE,
    COL_USERNAME,
)
from pdb.shared.constants import SALT_LEN
from typing import Any


class AuthManager:
    def __init__(
        self,
        db: DbConnector,
        sql: SqlCollection,
        hasher: HashAlgorithm,
        salter: Salter,
    ) -> None:
        self._db = db
        self._sql = sql
        self._hasher = hasher
        self._salter = salter

        self._hashers_map = {h.value: HasherFactory.create_hasher(h) for h in SupportedHash}
        self._salters_map = {s.value: SaltFactory.create_salter(s) for s in SupportedSalter}

    def authenticate(self, username: str, password: str) -> OpStatus:
        sql, params = self._sql.query_generator.create_query(TABLE_AUTH, conditions=[(COL_USERNAME, username)])

        user_entry = None
        try:
            results = self._db.read(sql, params)

            if results is None or len(results) <= 0:
                return OpStatus(False, f"User {username} not found - {ex}")

            user_entry = results[0]

        except Exception as ex:
            return OpStatus(False, f"Error reading user entry - {ex}")

        role = user_entry[1]
        pw_salt = user_entry[2]
        pw_hash = user_entry[3]
        pw_algo = user_entry[4]

        input_hash = self._hashers_map.get(pw_algo).hash(password, pw_salt)
        if input_hash != pw_hash:
            return OpStatus(False, f"Incorrect username/password")

        return OpStatus(True, f"Authenticated...")

    def add_user(self, username: str, password: str, role: str) -> OpStatus:
        pw_salt = self._salter.generate_salt(SALT_LEN)
        pw_hash = self._hasher.hash(password, pw_salt)

        sql, params = self._sql.insert_generator.generate_insert(
            TABLE_AUTH,
            [(COL_USERNAME, username), (COL_ROLE, role), (COL_PW_HASH, pw_hash), (COL_PW_SALT, pw_salt), (COL_PW_ALGO, self._hasher.name)],
        )

        try:
            self._db.write(sql, params)
            return OpStatus(True, "User added...")
        except Exception as ex:
            return OpStatus(False, f"Error adding user {username} - {ex}")

    def remove_user(self, username: str) -> OpStatus:
        sql, params = self._sql.delete_generator.generate_delete(TABLE_AUTH, [(COL_USERNAME, username)])
        try:
            self._db.write(sql, params)
            return OpStatus(True, "User removed...")
        except Exception as ex:
            return OpStatus(False, f"Error removing user {username} - {ex}")
