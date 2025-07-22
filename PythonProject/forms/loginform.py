from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired('Обязательно для заполнения')])
    password = PasswordField('Пароль', validators=[DataRequired('Без пароля не пройдешь')])
    not_robot = BooleanField('Я человек', validators=[DataRequired('Подтверди, что ты не робот')])
    submit = SubmitField('Войти')