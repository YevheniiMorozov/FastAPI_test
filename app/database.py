from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_USER = "postgres"
DB_PASS = "password"
IP = "database"
PORT = 5432
DB_NAME = "steam"


POSTGRES_URI = f"postgresql://{DB_USER}:{DB_PASS}@{IP}:{PORT}/{DB_NAME}"

engine = create_engine(POSTGRES_URI)
Session = sessionmaker()
