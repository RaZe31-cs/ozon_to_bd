from data.config import Client_Id, Apikey
import datetime
import requests
from data.models.data3 import Data3
from data.db_session import create_session, global_init
import schedule
import time
import logging

logging.basicConfig(format='%(asctime)s;%(levelname)s;%(message)s', level=logging.INFO, filename='root/log/app3.log',
                    filemode='w')


def add_3_api_to_db():
    logging.info('start')
    try:
        logging.info('get data')
        date = datetime.datetime.now() - datetime.timedelta(days=15)
        res = get_data_in_api3(date)
        logging.info('successful get data')
    except Exception as e:
        logging.error(e)
        return
    try:
        logging.info('connecting to the database')
        global_init('finance')
        sess = create_session()
        logging.info('successful connection to the database')
    except Exception as e:
        logging.info('unsuccessful connection to the database')
        logging.error(e)
        return
    count = 0
    print(res)
    for i in res['result']['rows']:
        data = Data3(
            date=datetime.datetime.now(),
            row_number=i['row_number'],
            product_id=i['product_id'],
            product_name=i['product_name'],
            barcode=i['barcode'],
            offer_id=i['offer_id'],
            commission_percent=i['commission_percent'],
            price=i['price'],
            price_sale=i['price_sale'],
            sale_amount=i['sale_amount'],
            sale_commission=i['sale_commission'],
            sale_discount=i['sale_discount'],
            sale_price_seller=i['sale_price_seller'],
            sale_qty=i['sale_qty'],
            return_sale=i['return_sale'],
            return_amount=i['return_amount'],
            return_commission=i['return_commission'],
            return_discount=i['return_discount'],
            return_price_seller=i['return_price_seller'],
            return_qty=i['return_qty']
        )
        try:
            sess.add(data)
            count += 1
            sess.commit()
        except Exception as e:
            logging.error(e)
    sess.close()
    logging.info(f'End, adding {count}')


def get_data_in_api3(date):
    url = 'https://api-seller.ozon.ru/v1/finance/realization'
    headers = {
        'Content-Type': 'application/json',
        'Client-Id': Client_Id,
        'Api-Key': Apikey
    }
    params = {
        'date': date.strftime('%Y-%m'),
    }
    response = requests.post(url, headers=headers, json=params)
    if response.status_code == 200:
        return response.json()
    return response.status_code


def main(t=False):
    if datetime.datetime.now().day == 6 or t:
        add_3_api_to_db()


if __name__ == '__main__':
    # global_init('finance')
    schedule.every().day.at("03:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
