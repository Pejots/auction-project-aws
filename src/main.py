from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='app/templates')

@app.route('/')
def index():
    #Renderiza página inicial
    return render_template('index.html', produtos = lista_produtos)

@app.route('/sales')
def sales():
    #Renderiza página de venda
    return render_template('/sales/sales.html')

@app.route('/sales/new')
def register_sale():
    return render_template('/sales/sales-new.html')

@app.route('/sales/create', methods=["POST"])
def new_product():
    #Lógica para criar produtos
    nameproduct = request.form['input-nameproduct']
    priceproduct = request.form['input-price']
    categoryproduct = request.form['select-category']
    datelimitproduct = request.form['input-datelimit']
    return jsonify({
        'status': 200,
        'text': f'{nameproduct} create successfully'
    })

@app.route('/sales/<id>')
def sale(id):
    #Renderiza página de cada produto em leilão
    return jsonify({
        'status':200,
        'text': f'Product is here!'
    })

@app.route('/user/login')
def login_user():
    #Renderiza página de login de usuário
    return render_template('/user/login.html')

@app.route('/user/auth', methods=["POST"])
def do_login():
    #Lógica para logar usuário
    user = request.form['input-username']
    return jsonify({
        'status': 200,
        'text': f'{user} login successfully'
    })

@app.route('/user/register')
def register_user():
    #Renderiza página de registro de usuário
    return render_template('/user/register.html')

@app.route('/user/new', methods=["POST"])
def new_user():
    user = request.form['input-username']
    #Lógica para registro de usuário
    return jsonify({
        'status': 200,
        'text': f'{user} register successfully'
    })

app.run(debug=True)