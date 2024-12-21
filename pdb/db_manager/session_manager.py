from datetime import timedelta
from pdb.database.connectors.db_connector import DbConnector
from pdb.database.sql.sql_collection import SqlCollection
from pdb.shared.op_status import OpStatus
from datetime import datetime
from pdb.db_manager.constants import TABLE_SESS, COL_SESS_TOKEN, COL_USERNAME, COL_EXP, COL_SESS_TOKEN
from pdb.shared.constants import SESSION_TOKEN_LEN
from pdb.tools.funcs import generate_random


class SessionManager:
    def __init__(self, db: DbConnector, sql: SqlCollection, session_timeout: timedelta) -> None:
        self._db = db
        self._sql = sql
        self._timeout = session_timeout

    def verify_session(self, session_token: str) -> OpStatus:
        sql, params = self._sql.query_generator.create_query(TABLE_SESS, conditions=[(COL_SESS_TOKEN, session_token)])
        try:
            results = self._db.read(sql, params)
            if results is None or len(results) <= 0:
                return OpStatus(False, f"Session Token not found...")

            session_entry = results[0]
            db_username = session_entry[0]
            db_token = session_entry[1]
            db_exp = session_entry[2]

            if datetime.now() > datetime.strftime(db_exp):
                return OpStatus(False, f"Session expired...")

            return OpStatus(True, db_username)

        except Exception as ex:
            return OpStatus(False, f"Error querying for session token - {ex}")

    def create_session(self, username: str) -> OpStatus:
        new_session_token = generate_random(SESSION_TOKEN_LEN)
        expiration = datetime.now() + self._timeout

        sql, params = self._sql.insert_generator.generate_insert(
            TABLE_SESS, [(COL_USERNAME, username), (COL_SESS_TOKEN, new_session_token), (COL_EXP, expiration)]
        )

        try:
            self._db.write(sql, params)
            return OpStatus(True, new_session_token)
        except Exception as ex:
            return OpStatus(False, f"Error creating session - {ex}")
