"""
Модуль приложения Flask для создания блога.

Модуль содержит объект приложения Flask, настройки базы данных и конфигурации.
Также включает настройки инструментов отладки, Toastr для вывода уведомлений,
LoginManager для управления авторизацией и конфигурации для загрузки файлов.

Атрибуты:
    app: Flask
        Объект приложения Flask.
    db: SQLAlchemy
        Объект базы данных SQLAlchemy.
    manager: LoginManager
        Объект LoginManager для управления авторизацией.
    toastr: Toastr
        Объект Toastr для вывода уведомлений.
    toolbar: DebugToolbarExtension
        Объект DebugToolbarExtension для настройки инструментов отладки.

Константы:
    UPLOAD_FOLDER: str
        Директория для загрузки файлов.
    ALLOWED_EXTENSIONS: set
        Разрешенные типы файлов для загрузки.
"""

import uuid

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr

app = Flask(__name__)

app.config['SECRET_KEY'] = str(uuid.uuid4())
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

manager = LoginManager(app)

toastr = Toastr(app)
app.config['TOASTR_SHOW_METHOD'] = 'show'
app.config['TOASTR_TIMEOUT'] = 5000

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024

toolbar = DebugToolbarExtension(app)
