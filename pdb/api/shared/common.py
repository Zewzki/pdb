from pdb.api.shared.constants import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_TYPE, DB_USER, HASH_TYPE, SALT_TYPE
from pdb.database.config.db_config import DbConfig
from pdb.database.connectors.connector_factory import ConnectorFactory
from pdb.shared.hash.hasher_factory import HasherFactory
from pdb.shared.salt.salt_factory import SaltFactory

db_config = DbConfig(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)
db = ConnectorFactory.create_connector(DB_TYPE)
hasher = HasherFactory.create_hasher(HASH_TYPE)
salter = SaltFactory.create_salter(SALT_TYPE)
