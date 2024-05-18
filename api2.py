import requests
from data.config import Apikey, Client_Id
import json
import datetime
from data.db_session import create_session, global_init
from sqlalchemy.exc import IntegrityError, OperationalError
import logging
import schedule
import time
from data.models.data2 import Data2

logging.basicConfig(format='%(asctime)s;%(levelname)s;%(message)s', level=logging.INFO, filename='root/log/app2.log',
                    filemode='a')
tz = datetime.timezone(datetime.timedelta(hours=3))


def get_data_in_api2(offset):
    url = 'https://api-seller.ozon.ru/v2/analytics/stock_on_warehouses'
    headers = {
        'Content-Type': 'application/json',
        'Client-Id': Client_Id,
        'Api-Key': Apikey}
    params = {
        "limit": 1000,
        "offset": offset,
        "warehouse_type": "ALL"
    }
    all_res = []
    res = requests.post(url, headers=headers, json=params)
    if res.status_code == 200:
        # while len(res.json()['result']['rows']) != 0:
        #     all_res.extend(res.json()['result']['rows'])
        #     params['offset'] += 1000
        #     res = requests.post(url, headers=headers, json=params)
        return res.json()['result']['rows']
    return res.status_code


def load_data_in_bd():
    offset = 0
    data = '00'
    while len(data) != 0:
        try:
            logging.info('Pars_ozon_api')
            data = get_data_in_api2(offset)
            offset += 1000
            logging.info('Pars successfully')
        except Exception:
            logging.info('Pars failed')
        try:
            global_init('db')
            db_sess = create_session()
        except Exception as e:
            logging.error(e)

        for i in data:
            try:
                sku_warehouse = f"{i['sku']}_{i['warehouse_name']}"
                data2 = Data2(sku_warehouse=sku_warehouse,
                              sku=i['sku'],
                              warehouse_name=i['warehouse_name'],
                              item_code=i['item_code'],
                              item_name=i['item_name'],
                              promised_amount=i['promised_amount'],
                              free_to_sell_amount=i['free_to_sell_amount'],
                              reserved_amount=i['reserved_amount'])
                db_sess.add(data2)
                db_sess.commit()
                logging.info('An entry has been added')
            except IntegrityError:
                logging.error('The record already exists')
                data2 = db_sess.query(Data2).filter(Data2.sku_warehouse == sku_warehouse).first()
                data2.load_data_time = datetime.datetime.now
                data2.sku = i['sku']
                data2.warehouse_name = i['warehouse_name']
                data2.item_code = i['item_code']
                data2.item_name = i['item_name']
                data2.promised_amount = i['promised_amount']
                data2.free_to_sell_amount = i['free_to_sell_amount']
                data2.reserved_amount = i['reserved_amount']
                db_sess.commit()
            except OperationalError:
                logging.error('Reconnecting to the database')
                global_init('db')
                db_sess = create_session()
            except Exception as e:
                print(e)
                logging.error(e)


if __name__ == '__main__':
    logging.info('Start')
    # global_init('db')
    schedule.every().day.at('05:00').do(load_data_in_bd)
    while True:
        schedule.run_pending()
        time.sleep(1)

# if __name__ == '__main__':
#     logging.info('Start')
#     try:
#         logging.info('Connect to database')
#         global_init('db')
#         logging.info('Successfully connect to database')
#     except Exception as e:
#         logging.error(e)
#     load_data_in_bd()
