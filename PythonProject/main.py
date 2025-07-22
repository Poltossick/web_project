import os.path

import requests
from openpyxl.styles.builtins import title
from pyexpat.errors import messages

from data import db_session
from forms.loginform import LoginForm
from forms.boardgames import GamesForm
from forms.players import Register
from flask import Flask, url_for, request, render_template, redirect, abort, make_response, jsonify
from werkzeug.utils import secure_filename, redirect
from data.users import Player
from data.games import Games
from data.teams import Teams
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

import sqlite3
from sqlite3 import Error


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SECRET_KEY'] = 'just_secret_key'
ALLOWED_EXTENSION = ['txt', 'pdf', 'jpg', 'png', 'csv', 'xlsx']

if __name__ == '__main__':
    db_session.global_init('database/games.sqlite')
    app.run(host='localhost', port=5000, debug=True)