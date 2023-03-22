import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = 'groups'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    max_messages = sqlalchemy.Column(sqlalchemy.Integer)
    mute_duration = sqlalchemy.Column(sqlalchemy.Integer)
