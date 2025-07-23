import datetime
from datetime import datetime

import os.path

import requests
from openpyxl.styles.builtins import title
from pyexpat.errors import messages

from forms.loginform import LoginForm
from forms.boardgames import GamesForm
from forms.players import Register
from flask import Flask, url_for, request, render_template, redirect, abort, make_response, jsonify
from werkzeug.utils import secure_filename, redirect
from data import db_session
from flask_restful import Api
from data.users import Player
from data.games import Games
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

import sqlite3
from sqlite3 import Error

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'you_never_coming'
login_manager = LoginManager()
login_manager.init_app(app)

@app.errorhandler(404)
def not_found(_):
    return make_response(({'error': 'Not found'}), 404)

@app.template_filter('str_to_datetime')
def str_to_datetime(s, format="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(s, format)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(Player, user_id)


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():  # то же самое, что и request.method == 'Post'
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   message='Пароли не совпадают', form=form)
        db_sess = db_session.create_session()
        if db_sess.query(Player).filter(Player.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   message='Такой пользователь уже зарегистрирован', form=form)
        user = Player(
            name=form.login.data,
            email=form.email.data,
            about=form.about.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html',
                           title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Player).filter(Player.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
        return render_template('login.html', title='Ошибка авторизации',
                               message='Неверный логин или пароль')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required  # не может зайти на страницу, пока не авторизируется
def logout():
    logout_user()
    return redirect('/login')


@app.route('/boardgames')
def show_games():
    db_sess = db_session.create_session()
    games = db_sess.query(Games).filter(Games.event_date >= datetime.now()).all()
    return render_template('games.html',
                           title='Настольные игры', games=games, datetime=datetime)


@app.route('/personal-page')
def personal_page():
    db_sess = db_session.create_session()
    my_games = db_sess.query(Games).filter(current_user == Games.owner).all()
    if current_user.is_authenticated:
        return render_template('personal-page.html',
                               title='Личная страница', games=my_games)
    else:
        abort(404)




@app.route('/gamesplay', methods=['POST', 'GET'])
@login_required
def add_boardgames():
    form = GamesForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        games = Games(name_game=form.name_game.data, content=form.content.data,
                      event_date=form.event_date.data, count_players=form.count_players.data)
        current_user.games.append(games)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/boardgames')
    return render_template('/gamesplay.html', title='Добавление игры', form=form)


@app.route('/gamesdelete/<int:id_num>', methods=['POST', 'GET'])
@login_required
def delete_game(id_num):
    db_sess = db_session.create_session()
    game = db_sess.query(Games).filter(
        Games.id == id_num, Games.owner == current_user
    ).first()
    if game:
        db_sess.delete(game)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/boardgames')


@app.route('/gamesplay/<int:id_num>', methods=['POST', 'GET'])
@login_required
def edit_game(id_num):
    form = GamesForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        game = db_sess.query(Games).filter(
            Games.id == id_num, Games.owner == current_user
        ).first()
        if game:
            form.name_game.data = game.name_game
            form.content.data = game.content
            form.event_date.data  = game.event_date
            form.count_players.data = game.count_players
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        game = db_sess.query(Games).filter(
            Games.id == id_num, Games.owner == current_user
        ).first()
        if game:
            game.name_game = form.name_game.data
            game.content = form.content.data
            game.event_date = form.event_date.data
            game.count_players = form.count_players.data
            db_sess.commit()
            return redirect('/boardgames')
        else:
            abort(404)
    return render_template('/gamesplay.html', title='Редактирование новости', form=form)

if __name__ == '__main__':
    db_session.global_init('database/news.sqlite')
    app.run(host='localhost', port=5000, debug=True)
