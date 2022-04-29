#MODELO CARROS
import datetime
import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

engine = sqlalchemy.create_engine("sqlite:///server.db")
connection = engine.connect()

Base = declarative_base(engine)

session = Session()

connection.execute(
    """CREATE TABLE IF NOT EXISTS CAR
    (
        ID INTEGER PRIMARY KEY
        ,NAME NVARCHAR(100)
        ,MODEL NVARCHAR(100)
        ,CAR_DESCRIPTION NVARCHAR(1000)
        ,USED NCHAR(1)
    )"""
)


class Car(Base):
    __tablename__ = 'CAR'
    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    name = Column('NAME', String(100))
    price = Column('MODEL', String(100))
    car_description = Column('CAR_DESCRIPTION', String(1000))
    used = Column('USED', CHAR(1))

    def __init__(self, name, model, car_description, used):
        self.name = name
        self.model = model
        self.car_description = car_description
        self.used = used