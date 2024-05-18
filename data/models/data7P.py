import sqlalchemy
from ..db_session import SqlAlchemyBase


class Data7P(SqlAlchemyBase):
    __tablename__ = 'perfomance'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_product = sqlalchemy.Column(sqlalchemy.Integer)
    title = sqlalchemy.Column(sqlalchemy.Text)
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    views = sqlalchemy.Column(sqlalchemy.Integer)
    clicks = sqlalchemy.Column(sqlalchemy.Integer)
    moneySpent = sqlalchemy.Column(sqlalchemy.Float)
    avgBid = sqlalchemy.Column(sqlalchemy.Float)
    orders = sqlalchemy.Column(sqlalchemy.Integer)
    ordersMoney = sqlalchemy.Column(sqlalchemy.Float)
    price_dynamic = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
