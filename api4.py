import requests
import datetime
import json
from data.config import Apikey, Client_Id
import logging
import sqlalchemy
import logging
from sqlalchemy.exc import IntegrityError, OperationalError
from data.models.data4 import Data4
from data.models.data4_items import Data4Items
from data.models.data4_services import Data4Services
from data.db_session import create_session, global_init
import schedule
import time
from sqlalchemy.orm import Session

logging.basicConfig(format='%(asctime)s;%(levelname)s;%(message)s', level=logging.INFO, filename='root/log/app4.log',
                    filemode='w')


def get_data_v3_finance_transaction_list(page=1):
    url = 'https://api-seller.ozon.ru/v3/finance/transaction/list'
    headers = {
        'Content-Type': 'application/json',
        'Client-Id': Client_Id,
        'Api-Key': Apikey
    }

    res = requests.post(url, headers=headers, json={
        "filter": {
            "date": {
                "from": f"{(datetime.datetime.now() - datetime.timedelta(days=30)).strftime(r'%Y-%m-%d')}T00:00:00.000Z",
                "to": f"{(datetime.datetime.now()).strftime(r'%Y-%m-%d')}T00:00:00.000Z",
            },
            "operation_type": [],
            "posting_number": "",
            "transaction_type": "all"
        },
        "page": page,
        "page_size": 1000
    })
    if res:
        return res.json()


def update_row(oper_id: int, sess: Session, item: dict):
    dict_update = {'operation_id': oper_id,
                   'operation_type': item['operation_type'],
                   'operation_date': item['operation_date'],
                   'operation_type_name': item['operation_type_name'],
                   'delivery_charge': item['delivery_charge'],
                   'return_delivery_charge': item['return_delivery_charge'],
                   'accruals_for_sale': item['accruals_for_sale'],
                   'sale_commission': item['sale_commission'],
                   'amount': item['amount'],
                   'type': item['type'],
                   'posting_delivery_schema': item['posting']['delivery_schema'],
                   'posting_order_date': item['posting']['order_date'],
                   'posting_posting_number': item['posting']['posting_number'],
                   'posting_warehouse_id': item['posting']['warehouse_id']}
    logging.info(f'Update main table with id {oper_id}')
    sess.query(Data4).filter(Data4.operation_id == oper_id).update(dict_update)


def load_data_in_db(data):
    logging.info('Pars_ozon')
    try:
        logging.info('Connect to database')
        global_init('finance')
        logging.info('Successfully connect to database')
    except Exception as e:
        logging.error(e)
    sess = create_session()
    for item in data['result']['operations']:
        try:
            if sess.query(Data4).filter(Data4.operation_id == item['operation_id']).first():
                update_row(item['operation_id'], sess, item)
            else:
                data4 = Data4(operation_id=item['operation_id'],
                              operation_type=item['operation_type'],
                              operation_date=item['operation_date'],
                              operation_type_name=item['operation_type_name'],
                              delivery_charge=item['delivery_charge'],
                              return_delivery_charge=item['return_delivery_charge'],
                              accruals_for_sale=item['accruals_for_sale'],
                              sale_commission=item['sale_commission'],
                              amount=item['amount'],
                              type=item['type'],
                              posting_delivery_schema=item['posting']['delivery_schema'],
                              posting_order_date=item['posting']['order_date'],
                              posting_posting_number=item['posting']['posting_number'],
                              posting_warehouse_id=item['posting']['warehouse_id'])
                sess.add(data4)
                sess.commit()
                for i in item['items']:
                    data4items = Data4Items(transaction_list_id=data4.id,
                                            name=i['name'],
                                            sku=i['sku'])
                    sess.add(data4items)
                for i in item['services']:
                    data4services = Data4Services(transaction_list_id=data4.id,
                                                  name=i['name'],
                                                  price=i['price'])
                    sess.add(data4services)
                sess.commit()
                logging.info('An entry has been added')
        except OperationalError:
            logging.error('Reconnecting to the database')
            global_init('finance')
            sess = create_session()
            logging.info('Successfully connect to database')
        except IntegrityError:
            sess.rollback()
            logging.info('Such a record already exists')
        # except Exception as e:
        #     print(e)
        #     logging.error(e)
    sess.close()


def main(flag=False):
    logging.info(f'Start pars_ozon day={datetime.datetime.now().day} if day=23')
    if datetime.datetime.now().day == 23 or flag:
        count = get_data_v3_finance_transaction_list(1)['result']['page_count']
        for i in range(1, count + 1):
            data = get_data_v3_finance_transaction_list(i)
            load_data_in_db(data)


if __name__ == '__main__':
    # global_init('finance')
    logging.info('Start')
    schedule.every().day.at('07:00').do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)

# if __name__ == '__main__':
#     main()
