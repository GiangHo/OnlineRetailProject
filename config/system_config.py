import os

# Postgres config
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = "postgres"
POSTGRES_PASS = ""
POSTGRES_DB = "retail_db"

# Data
ONLINE_RETAIL_FILE = "data/output_ecommerce_raw.csv"

# Logging
JB_LOG_DIR = "/var/log/"
INFO_LOG_NAME = "info"
JB_INFO_LOG_FILE = os.path.join(JB_LOG_DIR, "info.log")

ERROR_LOG_NAME = "error"
JB_ERROR_LOG_FILE = os.path.join(JB_LOG_DIR, "error.log")


