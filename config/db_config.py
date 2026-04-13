from config.system_config import *

DB_URI = "postgresql://{}:{}@localhost:5432/{}".format(
    POSTGRES_USER, POSTGRES_PASS, POSTGRES_DB
)