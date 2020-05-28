from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fe54a89f88d6c7ac6ec18f199c88f33a'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db: SQLAlchemy = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app) # Add functionality to db
loginManager.login_view='login' #Login as in the login route was created
loginManager.login_message_category='info'  #Info as in Bootstrap message style not the webpage
from flaskstudy1 import routes