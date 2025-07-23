# Введение во Flask
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
    games = Games()
    games = db_sess.query(Games).all()
    return render_template('games.html',
                           title='Настольные игры', games=games)


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


if __name__ == '__main__':
    db_session.global_init('database/news.sqlite')
    app.run(host='localhost', port=5000, debug=True)
