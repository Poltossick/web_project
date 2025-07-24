import datetime
import sqlalchemy
from  datetime import datetime
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Games(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'boardgames'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_game = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    event_date = sqlalchemy.Column(sqlalchemy.DateTime)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                    default=datetime.now())
    count_players = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    owner_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("players.id"))
    owner = orm.relationship('Player', back_populates="games")

    def __repr__(self):
        return f'{self.event_date}'



