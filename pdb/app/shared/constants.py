import os
from datetime import timedelta
from pdb.database.common import SupportedDb
from pdb.shared.hash.supported_hash import SupportedHash
from pdb.shared.salt.supported_salter import SupportedSalter

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_TYPE = SupportedDb(os.environ.get("DB_TYPE", "sqlite3"))
DB_DEBUG = os.environ.get("DB_DEBUG") == "True"

SESSION_TIMEOUT_HOURS = timedelta(hours=int(os.environ.get("SESSION_TIMEOUT_HOURS", 3)))

SALT_TYPE = SupportedSalter(os.environ.get("AUTH_SALT", "random"))
HASH_TYPE = SupportedHash(os.environ.get("AUTH_HASH", "sha256"))

HTML_ROOT = "./pdb/app/client/html"
