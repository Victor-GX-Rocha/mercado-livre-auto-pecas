""" Base for database conecatation. Create conection Engine. """

# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import AppConfigManager

config = AppConfigManager()

# url: str = "postgresql+psycopg2://postgres:123456@127.0.0.1:5432/mercado_livre_db"
url: str = config.database_url

engine = create_engine(url)
Base = declarative_base()
InternalSession = sessionmaker(bind=engine)

def init_database():
    """ Start the database """
    Base.metadata.create_all(engine)
    print("Starting database")
