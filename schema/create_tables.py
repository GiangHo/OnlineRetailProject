from sqlalchemy import create_engine, text

from config.db_config import DB_URI
from models import Base


# ===================== CREATE ENGINE =====================
engine = create_engine(DB_URI)


def create_schema():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS dwh;"))
        conn.commit()


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    print("Creating schema...")
    create_schema()

    print("Creating tables...")
    create_tables()

    print("Done!")
