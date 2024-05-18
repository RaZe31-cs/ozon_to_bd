from data.config import Client_Id, Apikey
from data.models.data5 import Data5
from data.db_session import create_session, global_init
import requests
import datetime
import time
from sqlalchemy.exc import IntegrityError, OperationalError
import logging
import schedule

logging.basicConfig(format='%(asctime)s;%(levelname)s;%(message)s', level=logging.INFO, filemode='w',
                    filename='root/log/app5.log')


def get_code():
    url = 'https://api-seller.ozon.ru/v1/report/postings/create'
    header = {'Client-Id': Client_Id, 'Api-Key': Apikey}
    params = {
        "filter": {
            "processed_at_from": f"{(datetime.datetime.now() - datetime.timedelta(days=14)).strftime('%Y-%m-%d')}T00:00:00Z",
            "processed_at_to": f"{datetime.datetime.now().strftime('%Y-%m-%d')}T00:00:00Z",
            "delivery_schema": ["fbo"],
            "sku": [],
            "cancel_reason_id": [],
            "offer_id": "",
            "status_alias": [],
            "statuses": [],
            "title": ""
        },
        "language": "EN"
    }
    response = requests.post(url, headers=header, json=params)
    if response:
        return response.json()['result']['code']


def get_link_csv(code):
    url = f'https://api-seller.ozon.ru/v1/report/info'
    header = {'Client-Id': Client_Id, 'Api-Key': Apikey}
    params = {
        "code": code
    }
    response = requests.post(url, headers=header, json=params)
    if response:
        if response.json()['result']['status'] == 'success':
            return response.json()['result']['file']
        return response.json()['result']['status']
    return response.status_code


def write_items_to_db(url):
    logging.info('Start_recording')
    global_init('db')
    sess = create_session()
    res = requests.get(url)
    text = res.iter_lines()
    for i in text:
        a = i.decode('utf-8').split(';')
        a = [i.replace('"', '') for i in a]
        try:
            data_5 = Data5(order_number_id=int(a[0].replace('-', '')),
                           Order_number=a[0],
                           Shipment_number=a[1],
                           Accepted_for_processing=a[2],
                           Shipment_date=a[3],
                           Status=a[4],
                           Delivery_date=a[5],
                           Actual_date_of_handing_over_to_delivery=a[6],
                           Shipment_amount=a[7],
                           Shipment_currency_code=a[8],
                           Product_name=a[9],
                           OZON_id=a[10],
                           Article_code=a[11],
                           Total_product_cost=a[12],
                           Product_currency_code=a[13],
                           Product_cost_for_customers=a[14],
                           Customer_currency_code=a[15],
                           Quantity=a[16],
                           Delivery_cost=a[17],
                           Linked_shipments=a[18],
                           Redemption_of_products=a[19],
                           Product_price_before_discounts=a[20],
                           Discount=a[21],
                           Discount_RUB=a[22],
                           Promotions=a[23],
                           Volumetric_product_weight_kg=a[24])
            sess.add(data_5)
            sess.commit()
            logging.info('Successful_recording')
        except IntegrityError:
            logging.error('IntegrityError')
            sess.rollback()
            entry = sess.query(Data5).filter(Data5.Order_number == a[0]).first()
            entry.Order_number = a[0]
            entry.Shipment_number = a[1]
            entry.Accepted_for_processing = a[2]
            entry.Shipment_date = a[3]
            entry.Status = a[4]
            entry.Delivery_date = a[5]
            entry.Actual_date_of_handing_over_to_delivery = a[6]
            entry.Shipment_amount = a[7]
            entry.Shipment_currency_code = a[8]
            entry.Product_name = a[9]
            entry.OZON_id = a[10]
            entry.Article_code = a[11]
            entry.Total_product_cost = a[12]
            entry.Product_currency_code = a[13]
            entry.Product_cost_for_customers = a[14]
            entry.Customer_currency_code = a[15]
            entry.Quantity = a[16]
            entry.Delivery_cost = a[17]
            entry.Linked_shipments = a[18]
            entry.Redemption_of_products = a[19]
            entry.Product_price_before_discounts = a[20]
            entry.Discount = a[21]
            entry.Discount_RUB = a[22]
            entry.Promotions = a[23]
            entry.Volumetric_product_weight_kg = a[24]
            sess.commit()
            logging.info('Successful_recording_update')
        except OperationalError:
            logging.error('OperationalError')
            global_init('db')
            sess = create_session()
        except Exception as e:
            logging.error(e)
    logging.info('End_recording')


def main():
    logging.info('Start_api5')
    code = get_code()
    link = get_link_csv(code)
    while '.csv' not in link:
        time.sleep(5)
        link = get_link_csv(code)
    write_items_to_db(link)


if __name__ == '__main__':
    # main()
    # global_init('db')
    logging.info('Start')
    schedule.every().day.at('01:00').do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
