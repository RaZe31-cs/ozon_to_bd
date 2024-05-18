import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase


class Data2(SqlAlchemyBase):
    __tablename__ = 'v2_analytics_stock_on_warehouses'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    load_data_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    sku_warehouse = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True, unique=True)
    sku = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    warehouse_name = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)
    item_code = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)
    item_name = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)
    promised_amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    free_to_sell_amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    reserved_amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)