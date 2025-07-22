import datetime
import sqlalchemy
from sqlalchemy.ext.hybrid import hybrid_property

from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

class Teams(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'teams'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    game_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("title.id"))
    game = orm.relationship('Games')
    event_date_id = sqlalchemy.Column(sqlalchemy.DateTime, sqlalchemy.ForeignKey("title.id"))
    event_date = orm.relationship('Games')
    owner_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("players.id"))
    owner = orm.relationship('Players')
    players = sqlalchemy.Column(sqlalchemy.String, nullable=True)


    def __repr__(self):
        return f' <Teams {self.game}: {self.event_date}>'

