from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_toastr import Toastr
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = 'jsdfhjsdhkjfkhsdfhlkjs'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

manager = LoginManager(app)

toastr = Toastr(app)
app.config['TOASTR_SHOW_METHOD'] = 'show'
app.config['TOASTR_TIMEOUT'] = 5000

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024

toolbar = DebugToolbarExtension(app)
