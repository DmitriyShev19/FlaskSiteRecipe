import datetime
from flask_login import UserMixin
from app import db, app, manager


class BaseModel:
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def save(self) -> None:
        """
        Сохраняет текущий экземпляр класса в базе данных

        :return: None
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create(cls, *args, **kwargs) -> 'BaseModel':
        """
        Позволяет создать новый объект в базе данных.

        :param args: Позиционные аргументы для передачи конструктору модели
        :type args: tuple
        :param kwargs: Аргументы ключевого слова для передачи конструктору модели.
        :type kwargs: dict
        :return: None
        """
        new_user = cls(*args, **kwargs)
        new_user.save()


class Users(db.Model, BaseModel, UserMixin):
    """
    Модель пользователя.

    :param id: уникальный идентификатор пользователя
    :type id: int
    :param login: логин пользователя
    :type login: str
    :param email: адрес электронной почты пользователя
    :type email: str
    :param password: пароль пользователя
    :type password: str
    :param created_at: дата и время создания записи о пользователе
    :type created_at: datetime
    """

    login = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Recipe(db.Model, BaseModel):
    """
    Модель рецепта.

    :param id: уникальный идентификатор рецепта
    :type id: int
    :param id_user: уникальный идентификатор пользователя, создавшего рецепт
    :type id_user: int
    :param dish_name: название блюда
    :type dish_name: str
    :param food_category: категория блюда
    :type food_category: str
    :param file_path: путь к файлу с изображением блюда
    :type file_path: str
    :param cooking_time: время приготовления блюда
    :type cooking_time: str
    :param ingredients: ингредиенты блюда
    :type ingredients: str
    :param recipe: инструкции по приготовлению блюда
    :type recipe: str
    :param created_at: дата создания рецепта
    :type created_at: datetime.datetime
    """

    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    dish_name = db.Column(db.String(100))
    food_category = db.Column(db.String(100))
    file_path = db.Column(db.String(700))
    cooking_time = db.Column(db.String(100))
    ingredients = db.Column(db.String(700))
    recipe = db.Column(db.String(1000))


@manager.user_loader
def load_user(user_id: int) -> Users | None:
    """
    Загружает пользователя из базы данных по заданному идентификатору.

    :param user_id: идентификатор пользователя
    :type user_id: int
    :return: объект пользователя, если пользователь существует, иначе None
    :rtype: Users
    """
    return Users.query.get(user_id)


with app.app_context():
    db.create_all()
