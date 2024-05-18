import sqlalchemy
from ..db_session import SqlAlchemyBase


class Data4Services(SqlAlchemyBase):
    __tablename__ = 'v3_finance_transaction_list_SERVICES'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    transaction_list_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('v3_finance_transaction_list.id'))
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)
    price = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)