from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets.core import DateInput, NumberInput


class GamesForm(FlaskForm):
    name_game = StringField('Название игры', validators=[DataRequired('Введите название игры')])
    content = TextAreaField('О чем игра?')
    event_date = DateInput('Дата проведения игры')
    count_players = NumberInput('Количество игроков')
    submit = SubmitField('Опубликовать')
