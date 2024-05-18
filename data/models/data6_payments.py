import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase


class Data6Payments(SqlAlchemyBase):
    __tablename__ = 'v1_finance_cash-flow-statement_list_payments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_v1_finance_cash_flow_statement_list = sqlalchemy.Column(sqlalchemy.Integer)
    payment = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    currency_code = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    