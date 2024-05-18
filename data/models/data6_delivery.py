import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase


class Data6Delivery(SqlAlchemyBase):
    __tablename__ = 'v1_finance_cash-flow-statement_list_delivery'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_v1_finance_cash_flow_statement_list = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=True)