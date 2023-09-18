from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeBase

DATABASE_URL = "sqlite:///./test.db"
DATABASE = Database(DATABASE_URL)
Base = DeclarativeBase()

def get_database():
    return DATABASE

def get_engine():
    return create_engine(DATABASE_URL)
