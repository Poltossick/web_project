from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.fields.simple import EmailField, TextAreaField
from wtforms.validators import DataRequired


class Register(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired('Введите свой email.')])
    password = PasswordField('Пароль', validators=[DataRequired('Придумайте пароль.')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired('Введите пароль повторно.')])
    login = StringField('Логин', validators=[DataRequired('Введите никнейм/имя/логин.')])
    about = TextAreaField('О себе')
    agreement = BooleanField('Согласие на обработку данных', validators=[DataRequired('Подтвердите согласие.')])
    submit = SubmitField('Регистрация')