from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired('Обязательно для заполнения')])
    password = PasswordField('Пароль', validators=[DataRequired('Без пароля не пройдешь')])
    submit = SubmitField('Войти')