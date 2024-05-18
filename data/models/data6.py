import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase


class Data6(SqlAlchemyBase):
    __tablename__ = 'v1_finance_cash-flow-statement_list'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date_write = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now().strftime('%Y-%m-%d'))
    period_begin = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    period_end = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    period_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    begin_balance_amount = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    delivery_total = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    delivery_amount = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    delivery_services_total = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    return_total = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    return_amount = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    return_services_total = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    loan = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    invoice_transfer = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    rfbs_total = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    rfbs_transfer_delivery = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    rfbs_transfer_delivery_return = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    rfbs_compensation_delivery_return = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    rfbs_partial_compensation = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    rfbs_partial_compensation_return = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    others_total = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    end_balance_amount = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    