import os
from datetime import datetime
from flask import request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import User, Recipe
from errors import *
from bisnes_logic import check_new_user, allowed_file


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index() -> Response | str:
    """
    Views для главной страницы.

    GET запрос:
    Возвращает главную страницу приложения, на которой отображаются все рецепты.

    :return: шаблон index.html с переданным списком рецептов.
    """
    receipts = Recipe.query.all()
    return render_template('index.html', receipts=receipts)


@app.route('/register/', methods=['GET', 'POST'])
def register() -> Response | str:
    """
    Views для страницы регистрации пользователя.

    GET запрос:
    Возвращает страницу с формой для регистрации.

    POST запрос:
    Извлекает из запроса login, email и password.
    Проверяет, что пользователь с таким логином и email еще не зарегистрирован в базе данных.
    Если проверка прошла успешно, то создает нового пользователя и перенаправляет его на страницу входа.
    В противном случае пользователю выводится сообщение об ошибке.

    :return: render_template(register.html) в случае GET запроса,
             redirect(url_for('input_user')) в случае успешной регистрации,
             render_template(register.html) в случае ошибки регистрации.
    """
    if request.method == 'GET':
        return render_template('register.html')
    login = request.form.get('login', '_')
    email = request.form.get('email')
    password = request.form.get('password', '_')
    if check_new_user(login=login, email=email, password=password):
        forms = dict(request.form)
        forms['password'] = generate_password_hash(password)
        User.create(**forms)
        return redirect(url_for('input_user'))
    else:
        return render_template('register.html')


@app.route('/input_user/', methods=['GET', 'POST'])
def input_user() -> Response | str:
    """
        Views для страницы входа пользователя.

        GET запрос:
        Возвращает страницу с формой для входа.

        POST запрос:
        Извлекает из запроса email и password.
        Если пользователь с такими данными найден в базе данных,
        то он аутентифицируется и перенаправляется на страницу аккаунта.
        В противном случае пользователю выводится сообщение об ошибке.

        :return: render_template(input_user.html) в случае GET запроса,
                 redirect(url_for('account_user')) в случае успешного входа,
                 render_template(input_user.html) в случае ошибки входа.
        """
    if request.method == 'GET':
        return render_template('input_user.html')
    email = request.form.get('email', '_')
    password = request.form.get('password', '_')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        flash({'title': 'Успешно!', 'message': 'Добро пожаловать'}, category='success')
        return redirect(url_for('account_user'))
    else:
        flash({"title": "Ошибка!", "message": "Мы не нашли такого пользователя"},
              category="error")
        return render_template('input_user.html')


@app.route('/account_user/', methods=['GET', 'POST'])
@login_required
def account_user():
    """
        Views для страницы аккаунта пользователя.
        Извлекает из базы данных рецепты пользователя с помощью его id.

        GET запрос:
        Возвращает страницу аккаунта пользователя, на которой отображены его рецепты.
        Если пользователь не аутентифицирован, перенаправляет на страницу входа.

        :return: render_template(account_user.html, recept_user=recept_user)
        """
    recept_user = Recipe.query.filter_by(id_user=current_user.id).all()
    return render_template('account_user.html', recept_user=recept_user)


@app.route('/open_recept/<int:recept_id>')
@login_required
def open_recept(recept_id):
    """
        Views для страницы отображения выбранного рецепта.

        GET запрос:
        Извлекает из запроса id рецепта.
        Если пользователь аутентифицирован и рецепт с таким id найден в базе данных,
        то пользователю выводится страница с детальной информацией о рецепте.
        В противном случае пользователю выводится сообщение об ошибке.

        :param recept_id: идентификатор рецепта.
        :type recept_id: int

        :return: render_template(open_recept.html, recept=recept) в случае успешного отображения рецепта
        """
    recept = Recipe.query.filter_by(id=recept_id).first()
    return render_template('open_recept.html', recept=recept)


@app.route('/firs_recipe/')
def firs_recipe():
    """
        Views для страницы с рецептами первых блюд.

        Возвращает страницу со списком всех рецептов первых блюд.

        :return: render_template(first_course_recipes.html, receipts=receipts)
    """
    receipts = Recipe.query.filter_by(food_category='Рецепты первых блюд').all()
    return render_template('first_course_recipes.html', receipts=receipts)


@app.route('/second_recipe/')
def second_recipe():
    """
            Views для страницы с рецептами вторых блюд.

            Возвращает страницу со списком всех рецептов вторых блюд.

            :return: render_template('second_course_recipes.html', receipts=receipts)
    """
    receipts = Recipe.query.filter_by(food_category='Рецепты вторых блюд').all()
    return render_template('second_course_recipes.html', receipts=receipts)


@app.route('/snake/')
def snake():
    """
            Views для страницы с рецептами закусок.

            Возвращает страницу со списком всех рецептов закусок.

            :return: return render_template('snack_recipes.html', receipts=receipts)
    """
    receipts = Recipe.query.filter_by(food_category='Рецепты закусок').all()
    return render_template('snack_recipes.html', receipts=receipts)


@app.route('/dough_recipes/')
def dough_recipes():
    """
        Views для страницы с рецептами изделий из текста.

        Возвращает страницу со списком всех рецептов изделий из теста.

        return render_template('dough_recipes.html', receipts=receipts)
    """
    receipts = Recipe.query.filter_by(food_category='Рецепты изделий из теста').all()
    return render_template('dough_recipes.html', receipts=receipts)


@app.route('/sweet_recipes/')
def sweet_recipes():
    """
        Views для страницы с рецептами сладостей.

        Возвращает страницу со списком всех рецептов сладостей.

        return render_template('sweet_recipes.html', receipts=receipts)
    """
    receipts = Recipe.query.filter_by(food_category='Рецепты сладостей').all()
    return render_template('sweet_recipes.html', receipts=receipts)


@app.route('/blank_recipes/')
def blank_recipes():
    """
        Views для страницы с рецептами заготовок.

        Возвращает страницу со списком всех рецептов сладостей.

        return render_template('snack_recipes.html', receipts=receipts)
    """
    receipts = Recipe.query.filter_by(food_category='Рецепты заготовок').all()
    return render_template('snack_recipes.html', receipts=receipts)


@app.route('/recipe_create/', methods=['GET', 'POST'])
@login_required
def recipe_create():
    """
        Views для создания рецепта.

        GET запрос:
        Возвращает страницу с формой для создания рецепта.

        POST запрос:
        Извлекает из запроса параметры, необходимые для создания рецепта:
        название блюда, id пользователя, категория блюда, время приготовления,
        список ингредиентов, список их количества и список мер, описание приготовления
        и изображение. Затем создает объект Recipe в базе данных и перенаправляет
        пользователя на страницу его аккаунта.

        :return: render_template('recipe_creation.html') в случае GET запроса,
                 redirect(url_for('account_user')) в случае успешного создания рецепта,
                 redirect('recipe_creation') в случае ошибки при создании рецепта.
    """
    if request.method == 'GET':
        return render_template('recipe_creation.html')
    dish_name = request.form.get('dish_name')
    id_user = current_user.id
    food_category = request.form.get('food_category')
    cooking_time = request.form.get('cooking_time')
    ingredient_list = request.form.getlist('ingredient')
    quantity_list = request.form.getlist('quantity')
    measure_list = request.form.getlist('measure')
    recipe_step = request.form.get('recipe')
    file = request.files['file']
    if file.filename == '':
        flash({"title": "Ошибка!", "message": "Вы не выбрали файл"})
        return redirect('recipe_creation')
    if file and allowed_file(file.filename):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = secure_filename(f"{timestamp}_{file.filename}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        ingredients_str = ';'.join([f'{ing},{qty},{meas}' for ing, qty, meas in
                                    zip(ingredient_list, quantity_list, measure_list)])
        Recipe.create(dish_name=dish_name, id_user=id_user, food_category=food_category, cooking_time=cooking_time,
                      ingredients=ingredients_str, recipe=recipe_step, file_path=file_path)
        return redirect(url_for('account_user'))


@app.route("/logout/")
@login_required
def logout():
    """
    Функция для выхода из профиля пользователя.

    :return: Response (всплывает сообщение о выходе и перекидывает на страницу авторизации)
    """
    flash({"title": "Успех", "message": "Вы вышли из аккаунта!"}, "success")
    logout_user()
    return redirect(url_for("index"))


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('input_user'))
    return response
