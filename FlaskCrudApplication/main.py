from cryptography.fernet import Fernet
import os
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

from app.models import User, Products, sessionDb

UPLOAD_FOLDER = './app/static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

application = Flask(__name__, template_folder="./app/templates",
                    static_folder="./app/static")
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

application.secret_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiTGVpbGFvUHJvaiIsInBhc3MiOiJ0ZXN0ZTEyMzMifQ.lJz3ZkWT7CzMjjw5-NXwK-_5xE5STTbBUFF2niBnu2U"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def verify_datecreated():
    products = sessionDb.query(Products)
    for product in products:
        if datetime.now() > (product.date_created + timedelta(days=3)):
            product_del = products.filter(Products.id == product.id).first()
            sessionDb.delete(product_del)
            sessionDb.commit()


verify_datecreated()


@application.route("/")
def index():
    print(session.get("logged_in"))
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template('index.html', cabecalho="Leilão online", lista_produtos=sessionDb.query(Products).limit(3), user_logged=session.get("logged_in"))


@application.route("/allproducts")
def all_products():
    return render_template('allproducts.html', cabecalho="Leilão online", lista_produtos=sessionDb.query(Products), user_logged=session.get("logged_in"))


@application.route("/novo-produto")
def novo_produto():
    # if session.get('logged_in'):
    #     return render_template("novo-produto.html", cabecalho="Novo Produto")
    # return render_template("login.html", cabecalho="Logar")
    return render_template("novo-produto.html", cabecalho="Novo Produto", user_logged=session.get("logged_in"))


@application.route("/criar", methods=["POST"])
def criar_produto():
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
                       descricaoProduto, categoriaProduto, filename)
    sessionDb.add(produto)
    sessionDb.commit()
    return redirect(url_for('index'))


@application.route("/comprar-produto/<id>", methods=["GET"])
def comprar(id: int):
    produto = sessionDb.query(Products).get(int(id))
    if produto != None:
        return render_template("comprar-produto.html",
                               cabecalho=produto.nome, produto=produto,
                               date_rest=(produto.date_created +
                                          timedelta(days=3) - datetime.now()),
                               user_logged=session.get("logged_in"),
                               price_prediction=round(produto.preco, 2)*1.0)
    return render_template("erro.html")

@application.route('/lance/<id>', methods=["POST"])
def give_bid(id: int):
    sessionDb.query(Products).filter(Products.id == id).update({"preco": request.form["inputPricePred"]})
    sessionDb.commit()
    return redirect(url_for('index'))

@application.route('/novo-user')
def novo_user():
    return render_template('registrar.html', cabecalho="Novo User")


@application.route('/criar-user', methods=['POST'])
def criar_usuario():
    nomeUser = request.form['nome']
    emailUser = request.form['email']
    key = Fernet.generate_key()
    senha = request.form['senha']
    senhaUser = Fernet(key).encrypt(senha.encode())

    if emailUser and senhaUser:
        user = User(nomeUser, emailUser, senhaUser)
        sessionDb.add(user)
        sessionDb.commit()
        session["logged_in"] = True
        return redirect(url_for('index'))

    return render_template('registrar.html', cabecalho="Registrar Usuário")


@application.route("/login")
def login():
    return render_template("login.html", cabecalho="Logar")


@application.route("/logar-usuario", methods=["GET", "POST"])
def logar():
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
        return redirect(url_for('index'))

    return render_template('login.html', cabecalho="Logar", alerta="Erro!", user_logged=session.get("logged_in"))


@application.route("/logout")
def deslogar():
    session["logged_in"] = False
    print(session.get("logged_in"))
    return redirect(url_for('login'))


application.run(debug=True)
