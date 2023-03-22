import sqlalchemy
from .db_session import SqlAlchemyBase


class SpamWords(SqlAlchemyBase):
    __tablename__ = 'spam_word'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    word = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=1)
