import datetime
import sqlalchemy


from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

class Teams(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'teams'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    game_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("boardgames.id"))
    game = orm.relationship('Games', viewonly=True)
    date = orm.relationship('Games')
    owner_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("players.id"))
    owner = orm.relationship('Player', back_populates="teams")
    players = sqlalchemy.Column(sqlalchemy.String, nullable=True)




