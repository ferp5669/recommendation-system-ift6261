from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'blablabla12334567'
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/rec'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Import at the end to avoid circular imports
from Rec import routes