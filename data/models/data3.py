import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase


class Data3(SqlAlchemyBase):
    __tablename__ = 'v1_finance_realization'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    # num = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    # doc_date = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    # contract_date = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    # contract_num = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    # currency_code = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    # doc_amount = sqlalchemy.Column(sqlalchemy.FLOAT)
    # vat_amount = sqlalchemy.Column(sqlalchemy.FLOAT)
    # payer_inn = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    # payer_kpp = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    # payer_name = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    # rcv_inn = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    # rcv_kpp = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    # rcv_name = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    # start_date = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    # stop_date = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    row_number = sqlalchemy.Column(sqlalchemy.INTEGER)
    product_id = sqlalchemy.Column(sqlalchemy.INTEGER)
    product_name = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    barcode = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    offer_id = sqlalchemy.Column(sqlalchemy.VARCHAR(250))
    commission_percent = sqlalchemy.Column(sqlalchemy.FLOAT)
    price = sqlalchemy.Column(sqlalchemy.FLOAT)
    price_sale = sqlalchemy.Column(sqlalchemy.FLOAT)
    sale_amount = sqlalchemy.Column(sqlalchemy.FLOAT)
    sale_commission = sqlalchemy.Column(sqlalchemy.FLOAT)
    sale_discount = sqlalchemy.Column(sqlalchemy.FLOAT)
    sale_price_seller = sqlalchemy.Column(sqlalchemy.FLOAT)
    sale_qty = sqlalchemy.Column(sqlalchemy.INTEGER)
    return_sale = sqlalchemy.Column(sqlalchemy.FLOAT)
    return_amount = sqlalchemy.Column(sqlalchemy.FLOAT)
    return_commission = sqlalchemy.Column(sqlalchemy.FLOAT)
    return_discount = sqlalchemy.Column(sqlalchemy.FLOAT)
    return_price_seller = sqlalchemy.Column(sqlalchemy.FLOAT)
    return_qty = sqlalchemy.Column(sqlalchemy.INTEGER) 
