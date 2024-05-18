import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase
import sqlalchemy


class Data5(SqlAlchemyBase):
    __tablename__ = 'v1_report_info'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    order_number_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True)
    date_write = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    Order_number = sqlalchemy.Column(sqlalchemy.Text)
    Shipment_number = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Accepted_for_processing = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Shipment_date = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Status = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Delivery_date = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Actual_date_of_handing_over_to_delivery = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Shipment_amount = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Shipment_currency_code = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Product_name = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    OZON_id = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Article_code = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Total_product_cost = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Product_currency_code = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Product_cost_for_customers = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Customer_currency_code = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Quantity = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Delivery_cost = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Linked_shipments = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Redemption_of_products = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Product_price_before_discounts = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Discount = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Discount_RUB = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Promotions = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    Volumetric_product_weight_kg = sqlalchemy.Column(sqlalchemy.Text, nullable=True)