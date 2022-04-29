# MODELO VENDA
import datetime
import sqlalchemy
from sqlalchemy import Column, Integer, String, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

engine = sqlalchemy.create_engine("sqlite:///server.db")
connection = engine.connect()

Base = declarative_base(engine)

session = Session()

connection.execute(
    """CREATE TABLE IF NOT EXISTS SALES
    (
        ID INTEGER PRIMARY KEY
        ,ID_AUCTION INTEGER        
    )"""
)


class Sale(Base):
    __tablename__ = 'SALES'
    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    id_action = Column('ID_AUCTION', Integer)

    def __init__(self, id_action):
        self.id_action = id_action