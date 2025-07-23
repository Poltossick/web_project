from datetime import datetime

from flask import app

from data import db_session
from data.games import Games
from data.users import Player
from data.teams import Teams

db_session.global_init('database/news.sqlite')
event = Games()
db_sess = db_session.create_session()
event = db_sess.query(Games).all()
for item in event:
    if datetime.strptime(str(item), "%Y-%m-%d %H:%M:%S") <= datetime.now():
        print(item)


