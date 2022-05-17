from flask import Flask
from flask_login import LoginManager

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI']  = 'mysql://root:secret@localhost/projetoleilao'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
application.config["JWT_COOKIE_SECURE"] = False
application.config["SECRET_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiQmFycm9zIiwic2VuaGEiOiJHYWJyaWVsMzQ1NiJ9.VZ-uGhnlN6TtkeuhmjMTlP4xwx1BNPwQp9reBzPV_yc"

login_manager = LoginManager(application)