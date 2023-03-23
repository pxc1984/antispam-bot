import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase


class Users(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    first_name = sqlalchemy.Column(sqlalchemy.String)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True)
    is_bot = sqlalchemy.Column(sqlalchemy.Boolean)
    
    weight = sqlalchemy.Column(sqlalchemy.Integer)
