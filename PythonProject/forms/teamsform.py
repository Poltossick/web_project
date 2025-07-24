from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField


class TeamForm(FlaskForm):
    players = BooleanField('Участвовать в игре')
    submit = SubmitField('Подтвердите участие')
