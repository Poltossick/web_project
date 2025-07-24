from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms import IntegerField, DateField
from wtforms.widgets import NumberInput, DateInput



class GamesForm(FlaskForm):
    name_game = StringField('Название игры', validators=[DataRequired('Введите название игры')])
    content = TextAreaField('О чем игра?')
    event_date = DateField('Дата проведения игры', widget=DateInput())
    count_players = IntegerField('Количество игроков', widget=NumberInput())
    submit = SubmitField('Опубликовать')
