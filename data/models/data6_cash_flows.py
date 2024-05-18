import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase


class Data6CashFlows(SqlAlchemyBase):
    __tablename__ = 'v1_finance_cash-flow-statement_list_cash_flows'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_v1_finance_cash_flow_statement_list = sqlalchemy.Column(sqlalchemy.Integer)
    commission_amount = sqlalchemy.Column(sqlalchemy.Float)
    currency_code = sqlalchemy.Column(sqlalchemy.Text)
    item_delivery_and_return_amount = sqlalchemy.Column(sqlalchemy.Float)
    orders_amount = sqlalchemy.Column(sqlalchemy.Float)
    period_begin = sqlalchemy.Column(sqlalchemy.Text)
    period_end = sqlalchemy.Column(sqlalchemy.Text)
    period_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    returns_amount = sqlalchemy.Column(sqlalchemy.Float)
    services_amount = sqlalchemy.Column(sqlalchemy.Float)
    