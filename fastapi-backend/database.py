from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import event

SQLITE_FILE_NAME = "db.sqlite3"
DATABASE_URL = f"sqlite:///./{SQLITE_FILE_NAME}"

CONNECT_ARGS = {
    "check_same_thread": False,
}
engine = create_engine(DATABASE_URL, connect_args=CONNECT_ARGS)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def close_db():
    engine.dispose()