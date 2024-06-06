from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECREye3%$^@*rurprbeysr'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
Login_manager = LoginManager(app)
Login_manager.login_view = 'login'
Login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)
from website import routes