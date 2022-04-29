import datetime
import sqlalchemy
from sqlalchemy import Column, Integer, String, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# MODELO PIECES
engine = sqlalchemy.create_engine("sqlite:///server.db")
connection = engine.connect()

Base = declarative_base(engine)

session = Session()

connection.execute(
    """CREATE TABLE IF NOT EXISTS PIECES
    (
        ID INTEGER PRIMARY KEY
        ,NAME NVARCHAR(100)        
        ,PIECES_DESCRIPTION NVARCHAR(1000)
        ,USED NCHAR(1)
    )"""
)


class Pieces(Base):
    __tablename__ = 'PIECES'
    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    name = Column('NAME', String(100))
    pieces_description = Column('PIECES_DESCRIPTION', String(100))
    used = Column('USED', CHAR(1))

    def __init__(self, name, pieces_description, used):
        self.name = name
        self.pieces_description = pieces_description
        self.used = used