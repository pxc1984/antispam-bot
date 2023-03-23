import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = 'groups'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    is_forum = sqlalchemy.Column(sqlalchemy.Boolean)
    title = sqlalchemy.Column(sqlalchemy.String)
    
    max_messages = sqlalchemy.Column(sqlalchemy.Integer)
    mute_duration = sqlalchemy.Column(sqlalchemy.Integer)
