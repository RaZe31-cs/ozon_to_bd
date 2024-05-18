import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase


class Data4(SqlAlchemyBase):
    __tablename__ = 'v3_finance_transaction_list'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                             default=datetime.datetime.now)
    operation_id = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)
    operation_type = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)
    operation_date = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)
    operation_type_name = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)
    delivery_charge = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    return_delivery_charge = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    accruals_for_sale = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    sale_commission = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    amount = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)
    posting_delivery_schema = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)
    posting_order_date = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)
    posting_posting_number = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)
    posting_warehouse_id = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)