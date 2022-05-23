from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

# CONFIGURAR CONEXÃO COM BANCO DE DADOS SQLITE
engine = create_engine("sqlite:///server.db",
                       connect_args={'check_same_thread': False})
connection = engine.connect()

# INICIAR SESSÃO COM BANCO DE DADOS
sessionDb = Session()

# INSTANCIAR CLASSE BASE DO SQLALCHEMY
Base = declarative_base(engine)


class User(Base):
    __tablename__ = 'USERS'
    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String(255), nullable=False)
    email = Column('email', String(255), nullable=False)
    senha = Column('senha', String(255), nullable=False)
    # Método construtor

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha


connection.execute('''CREATE TABLE IF NOT EXISTS USERS(
                              ID INTEGER PRIMARY KEY,
                              nome VARCHAR(255),
                              email VARCHAR(255),
                              senha VARCHAR(255)
                              )''')


class Products(Base):
    __tablename__ = 'PRODUCTS'
    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    id_user_created = Column('ID_USER_CREATED', Integer, nullable=True)
    id_bid = Column('ID_USER_BID', Integer, nullable=True)
    nome = Column('nome_prod', String(255), nullable=False)
    preco = Column('preco_prod', Float, nullable=False)
    desc = Column('descricao_prod', String(255), nullable=False)
    categoria = Column('categoria_prod', Text, nullable=False)
    date_created = Column('date_created', DateTime, default=datetime.now())
    img = Column('imagem_prod', String(255),
                 nullable=False, default="produto-nulo.png")

    def __init__(self, nome_prod, preco_prod, descricao_prod, categoria_prod, imagem_prod, id_user_created=None, id_bid=None):
        self.id_user_created = id_user_created
        self.id_bid = id_bid
        self.nome = nome_prod
        self.preco = preco_prod
        self.desc = descricao_prod
        self.categoria = categoria_prod
        self.img = imagem_prod


connection.execute('''CREATE TABLE IF NOT EXISTS PRODUCTS(
                              ID INTEGER PRIMARY KEY,
                              ID_USER_CREATED Integer,
                              ID_USER_BID Integer,
                              nome_prod VARCHAR(255),
                              preco_prod Decimal(10,2),
                              descricao_prod Text,
                              categoria_prod VARCHAR(20),
                              date_created DateTime,
                              imagem_prod VARCHAR(255)
                              )''')


class ProductsSell(Base):
    __tablename__ = 'PRODUCTS_SELL'
    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    id_user_created = Column('ID_USER_CREATED', Integer, nullable=True)
    id_bid = Column('ID_USER_BID', Integer, nullable=True)

    def __init__(self, id_user_created, id_bid):
        self.id_user_created = id_user_created
        self.id_bid = id_bid


connection.execute('''CREATE TABLE IF NOT EXISTS PRODUCTS_SELL(
                              ID INTEGER PRIMARY KEY,
                              ID_USER_CREATED Integer,
                              ID_USER_BID Integer
                              )''')
