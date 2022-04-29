import datetime
import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# MODELO LANCES
engine = sqlalchemy.create_engine("sqlite:///server.db")
connection = engine.connect()

Base = declarative_base(engine)

session = Session()

connection.execute(
    """CREATE TABLE IF NOT EXISTS AUCTION
    (
        ID INTEGER PRIMARY KEY
        ,ID_CAR INTEGER
        ,ID_PIECES INTEGER
        ,NAME NVARCHAR(100)
        ,PRICE DECIMAL(20,2)
        ,CATEGORY NVARCHAR(10)
        ,DATE_CREATE DATETIME
        ,DATE_LIMIT DATETIME
    )"""
)


class Auction(Base):
    __tablename__ = 'AUCTION'
    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    id_car = Column('ID_Car', Integer)
    id_pieces = Column('ID_PIECES', Integer)
    name = Column('NAME', String(255))
    price = Column('PRICE', Float(10, 2))
    category = Column('CATEGORY', String(10))
    date_create = Column('DATE_CREATE', default=datetime.datetime.utcnow)
    date_limit = Column('DATE_LIMIT', DateTime())

    def __init__(self, name, price, category, date_limit, id_car = None, id_pieces = None):
        self.id_car = id_car
        self.id_pieces = id_pieces
        self.name = name
        self.price = price
        self.category = category
        self.date_limit = date_limit
