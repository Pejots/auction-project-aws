# -*- coding: utf-8 -*-
from waitress import serve
from cryptography.fernet import Fernet
import os
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import jsonpickle

from app.models import ProductsSell, User, Products, sessionDb

UPLOAD_FOLDER = './app/static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

application = Flask('__name__', template_folder="./app/templates",
                    static_folder="./app/static")
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

application.secret_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiTGVpbGFvUHJvaiIsInBhc3MiOiJ0ZXN0ZTEyMzMifQ.lJz3ZkWT7CzMjjw5-NXwK-_5xE5STTbBUFF2niBnu2U"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def verify_datecreated():
    products = sessionDb.query(Products)
    for product in products:
        if datetime.now() > (product.date_created + timedelta(days=1)):
            product_del = products.filter(Products.id == product.id).first()
            if product_del.id_bid != None:
                product_sell = ProductsSell(
                    product_del.id_user_created, product_del.id_bid)
                sessionDb.add(product_sell)
                sessionDb.commit()
            if product_del.img != "produto-nulo.png":
                os.remove(
                    application.config['UPLOAD_FOLDER']+"/"+product_del.img.decode())
            sessionDb.delete(product_del)
            sessionDb.commit()


def get_info_user(id):
    user = sessionDb.query(User).filter(User.id == id).first()
    user_json = jsonpickle.encode(user)
    return user_json


@application.route("/")
def index():
    verify_datecreated()

    try:
        user = jsonpickle.decode(session.get("user"))
    except:
        user = ""
    return render_template('index.html', cabecalho="Leilão online", lista_produtos=sessionDb.query(Products).limit(3), user_logged=session.get("logged_in"), user_infos=user)


@application.route("/allproducts")
def all_products():
    verify_datecreated()
    try:
        user = jsonpickle.decode(session.get("user"))
    except:
        user = ""
    return render_template('allproducts.html', cabecalho="Leilão online", lista_produtos=sessionDb.query(Products), user_logged=session.get("logged_in"), user_infos=user)


@application.route("/novo-produto")
def novo_produto():
    verify_datecreated()
    if session.get('logged_in'):
        return render_template("novo-produto.html", cabecalho="Novo Produto", user_logged=session.get("logged_in"), user_infos=jsonpickle.decode(session.get("user")))
    return render_template("login.html", cabecalho="Logar", alerta="Usuário precisa de login!")


@application.route("/criar", methods=["POST"])
def criar_produto():
    verify_datecreated()
    creator = jsonpickle.decode(session.get("user"))
    nomeProduto = request.form["nome"]
    precoProduto = request.form["preco"]
    descricaoProduto = request.form["descricao"]
    categoriaProduto = request.form["categoria"]
    filename = "produto-nulo.png"
    if request.method == 'POST':
        file = request.files['imgProduto']
        if file and allowed_file(file.filename):
            key = Fernet.generate_key()
            filename = Fernet(key).encrypt(
                secure_filename(file.filename).encode())
            file.save(os.path.join(
                application.config['UPLOAD_FOLDER'], filename.decode()).replace("\\", "/"))
    produto = Products(nomeProduto, precoProduto,
                       descricaoProduto, categoriaProduto, filename, creator.id)
    sessionDb.add(produto)
    sessionDb.commit()
    return redirect(url_for('index'))


@application.route("/comprar-produto/<id>", methods=["GET"])
def comprar(id):
    try:
        user = jsonpickle.decode(session.get("user"))
    except:
        user = ""
    verify_datecreated()
    produto = sessionDb.query(Products).get(int(id))
    if produto != None:
        while produto.date_created+timedelta(days=1)-datetime.now() != 0:
            time = produto.date_created+timedelta(days=1)-datetime.now()
            return render_template("comprar-produto.html",
                                   cabecalho=produto.nome, produto=produto, creator=jsonpickle.decode(
                                       get_info_user(produto.id_user_created)),
                                   date_rest=time,
                                   user_logged=session.get("logged_in"),
                                   user_infos=user,
                                   price_prediction=round(produto.preco, 2)*1.0)
    return render_template("erro.html")


@application.route('/lance/<id>', methods=["POST"])
def give_bid(id):
    verify_datecreated()
    if session.get("logged_in"):
        buyer = jsonpickle.decode(session.get("user"))
        sessionDb.query(Products).filter(Products.id == int(id)).update(
            {"preco": request.form["inputPricePred"], "id_bid": buyer.id})
        sessionDb.commit()
        return redirect(url_for('index'))
    return render_template("login.html", cabecalho="Logar", alerta="Usuário precisa de login!")


@application.route('/novo-user')
def novo_user():
    verify_datecreated()
    return render_template('registrar.html', cabecalho="Novo User")


@application.route('/criar-user', methods=['POST'])
def criar_usuario():
    verify_datecreated()
    nomeUser = request.form['nome']
    emailUser = request.form['email']
    key = Fernet.generate_key()
    senha = request.form['senha']
    senhaUser = Fernet(key).encrypt(senha.encode())

    if emailUser and senhaUser:
        user = User(nomeUser, emailUser, senhaUser)
        sessionDb.add(user)
        sessionDb.commit()
        return redirect(url_for('login'))

    return render_template('registrar.html', cabecalho="Registrar Usuário")


@application.route("/login")
def login():
    verify_datecreated()
    return render_template("login.html", cabecalho="Logar")


@application.route("/logar-usuario", methods=["GET", "POST"])
def logar():
    verify_datecreated()
    if request.method == "POST":
        usuario = {
            'email': request.form['email'],
            'senha': request.form['senha']
        }

        key = Fernet.generate_key()

        fernet = Fernet(key)

        user = sessionDb.query(User).filter(
            User.email == usuario["email"] and fernet.decrypt(User.senha) == usuario["senha"]).first()
        if not user:
            return render_template('login.html', cabecalho="Logar", alerta="Usuário não existe!")
        session["logged_in"] = True
        session["user"] = get_info_user(user.id)
        return redirect(url_for('index'))

    return render_template('login.html', cabecalho="Logar", alerta="Erro!")


@application.route("/logout")
def deslogar():
    verify_datecreated()
    session["logged_in"] = False
    return redirect(url_for('login'))


if __name__ == "__main__":
    serve(application, host='0.0.0.0', port=80)
# application.run(debug=True)
