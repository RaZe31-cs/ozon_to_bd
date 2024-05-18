from data.config import Cliend_id_perfomance, Apikey_perfomance
from data.db_session import global_init, create_session
from data.models.data7P import Data7P
import requests
import json
import datetime
import logging
import schedule
import time

logging.basicConfig(format='%(asctime)s;%(levelname)s;%(message)s', level=logging.INFO, filemode='w',
                    filename='root/log/app7p.log')


def connect_to_bd(name_db):
    try:
        logging.info('Connecting to the database')
        global_init(name_db)
        logging.info('Successful connection to the database')
    except Exception as e:
        logging.info('Error connecting to the database')
        logging.error(e)


def get_access_token():
    url = 'https://performance.ozon.ru/api/client/token'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    params = {
        'client_id': Cliend_id_perfomance,
        'client_secret': Apikey_perfomance,
        "grant_type": "client_credentials"
    }
    res = requests.post(url, headers=headers, json=params)
    if res:
        return res.json()['access_token'], res.json()['token_type']
    return res.status_code


def write_data():
    logging.info('Running the script')
    logging.info('Get access_token and token_type')
    now_date = datetime.datetime.now()
    access_token, token_type = get_access_token()
    print(access_token, token_type)
    logging.info(f'{token_type} {access_token}')
    url = 'https://performance.ozon.ru:443/api/client/statistics/daily/json'
    headers = {
        'Authorization': f'{token_type} {access_token}',
        'Content-Type': 'application/json'
    }
    params = {'dateFrom': f'{(now_date - datetime.timedelta(hours=1)).strftime(r"%Y-%m-%d")}',
              'dateTo': f'{(now_date).strftime(r"%Y-%m-%d")}'}
    logging.info(f'Get dateFrom-{params["dateFrom"]}, dateTo-{params["dateTo"]}')
    res = requests.get(url, headers=headers, params=params)
    if res:
        logging.info('Successful request')
        data = res.json()['rows']
        write_in_db(data)
    else:
        logging.info('Error request')
        logging.info(str(res.status_code))


def write_in_db(res_list_dict):
    global_init('perfomance_api')
    session = create_session()
    logging.info('Writing data to the database')
    count = 0
    for i in res_list_dict:
        try:
            old_data7p = session.query(Data7P).filter(Data7P.id_product == int(i['id'])).order_by(
                Data7P.id.desc()).first()
            logging.info(f'Get old data7p {old_data7p}')
        except Exception as e:
            logging.info('Error reading data from the database')
            logging.error(e)
            connect_to_bd('perfomance_api')
            session = create_session()
            old_data7p = session.query(Data7P).filter(Data7P.id_product == int(i['id'])).order_by(
                Data7P.id.desc()).first()
            logging.info(f'Get old data7p {old_data7p}')
        if old_data7p is not None:
            price_dynamic = float(i['moneySpent'].replace(',', '.')) - old_data7p.moneySpent
            logging.info(f'price_dynamic is {price_dynamic}')
        else:
            price_dynamic = None
        data7p = Data7P(id_product=int(i['id']),
                        title=i['title'],
                        date=datetime.datetime.strptime(i['date'], '%Y-%m-%d'),
                        views=int(i['views']),
                        clicks=int(i['clicks']),
                        moneySpent=float(i['moneySpent'].replace(',', '.')),
                        avgBid=float(i['avgBid'].replace(',', '.')),
                        orders=int(i['orders']),
                        ordersMoney=float(i['ordersMoney'].replace(',', '.')),
                        price_dynamic=price_dynamic)
        session.add(data7p)
        try:
            session.commit()
            count += 1
        except Exception as e:
            logging.info('Error writing data to the database')
            logging.error(e)
            session.close()
    logging.info(f'Successfully written {count} data to the database')
    session.close()


if __name__ == '__main__':
    # write_data()
    # global_init('perfomance_api')
    logging.info('Start')
    schedule.every(1).hours.do(write_data)
    while True:
        schedule.run_pending()
        time.sleep(1)
