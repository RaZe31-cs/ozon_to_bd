import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase

 
class Data(SqlAlchemyBase):
    __tablename__ = 'data'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date_and_sku = sqlalchemy.Column(sqlalchemy.VARCHAR(250), unique=True, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    sku = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    sku_name = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)
    revenue = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    ordered_units = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hits_view_search = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hits_view_pdp = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hits_view = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hits_tocart_search = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hits_tocart_pdp = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hits_tocart = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    session_view_search = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    session_view_pdp = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    session_view = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    conv_tocart_search = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    conv_tocart_pdp = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    conv_tocart = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    returns = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    cancellations = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    delivered_units = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    position_category = sqlalchemy.Column(sqlalchemy.VARCHAR(250), nullable=True)