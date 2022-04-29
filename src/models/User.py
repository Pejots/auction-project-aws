# MODELO USUÁRIO
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

engine = sqlalchemy.create_engine("sqlite:///server.db")
connection = engine.connect()

Base = declarative_base(engine)

session = Session()

connection.execute(
    """CREATE TABLE IF NOT EXISTS USER
    (
        ID INTEGER PRIMARY KEY
        ,NAME NVARCHAR(100)
        ,EMAIL NVARCHAR(100)
        ,PASSWORD NVARCHAR(100)
    )"""
)


class User(Base):
    __tablename__ = 'USER'
    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    name = Column('NAME', String(100))
    email = Column('EMAIL', String(100))
    password = Column('PASSWORD', String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
