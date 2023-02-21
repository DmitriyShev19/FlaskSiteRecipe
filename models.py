import datetime
from flask_login import UserMixin
from app import db, app, manager


class BaseModel:
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create(cls, *args, **kwargs):
        new_user = cls(*args, **kwargs)
        new_user.save()


class Users(db.Model, BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


class Recipe(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    dish_name = db.Column(db.String(100))
    food_category = db.Column(db.String(100))
    file_path = db.Column(db.String(700))
    cooking_time = db.Column(db.String(100))
    ingredients = db.Column(db.String(700))
    recipe = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


with app.app_context():
    db.create_all()

