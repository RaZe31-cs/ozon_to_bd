import requests
import datetime
import os
from data.config import Client_Id, Apikey
from data.models.data import Data
from data.db_session import create_session, global_init
import schedule
import time
import logging
from sqlalchemy.exc import IntegrityError, OperationalError

logging.basicConfig(format='%(asctime)s;%(levelname)s;%(message)s', level=logging.INFO, filename='root/log/app.log',
                    filemode='w')
tz = datetime.timezone(datetime.timedelta(hours=3))


class Except_NoData(Exception):
    pass


def get_write(data_and_sku, response2):
    try:
        for j in response2['result']['data']:
            if j['dimensions'][1]['id'] + '_' + j['dimensions'][0]['id'] == data_and_sku:
                return j['metrics']
        else:
            return None
    except KeyError:
        raise Except_NoData


params = {"date_from": 'date_from',
          "date_to": 'date_to',
          "metrics": ["revenue",
                      "ordered_units",
                      'hits_view_search',
                      "hits_view_pdp",
                      "hits_view",
                      "hits_tocart_search",
                      "hits_tocart_pdp",
                      "hits_tocart",
                      "session_view_search"
                      ],
          "dimension": [
              "sku",
              "day"
          ],
          "filters": [],
          "sort": [
              {
                  "key": "revenue",
                  "order": "DESC"
              }
          ],
          "limit": 1000,
          "offset": 'i * 1000'}


def get_data(url, i):
    date_to = datetime.datetime.now(tz=tz).strftime("%Y-%m-%d")
    date_from = (datetime.datetime.now(tz=tz) - datetime.timedelta(days=14)).strftime("%Y-%m-%d")
    headers = {"contentType": "application/json",
               'Client-Id': Client_Id,
               'Api-Key': Apikey}
    params['date_from'] = date_from
    params['date_to'] = date_to
    params['offset'] = i * 1000
    params['metrics'] = ["revenue",
                         "ordered_units",
                         'hits_view_search',
                         "hits_view_pdp",
                         "hits_view",
                         "hits_tocart_search",
                         "hits_tocart_pdp",
                         "hits_tocart",
                         "session_view_search"
                         ]
    response = requests.post(url, headers=headers, json=params)
    while response.status_code != 200 and response.status_code == 429:
        logging.info('Слишком частые запросы, ждем 60 секунд')
        time.sleep(60)
        response = requests.post(url, headers=headers, json=params)
    params["metrics"] = ["revenue",
                         "session_view_pdp",
                         "session_view",
                         'conv_tocart_search',
                         "conv_tocart_pdp",
                         "conv_tocart",
                         "returns",
                         "cancellations",
                         "delivered_units",
                         "position_category"
                         ]
    response2 = requests.post(url, headers=headers, json=params)
    while response2.status_code != 200 and response2.status_code == 429:
        logging.info('Слишком частые запросы, ждем 60 секунд')
        time.sleep(60)
        response2 = requests.post(url, headers=headers, json=params)
    return response.json(), response2.json()


def main():
    logging.info('Start import')
    count_existing = 0
    count = 0

    url = 'https://api-seller.ozon.ru/v1/analytics/data'
    for i in range(1, 20):
        response1, response2 = get_data(url, i)
        try:
            logging.info('connecting to the database')
            global_init('db')
            sess = create_session()
            logging.info('connecting to the database successfully')
        except Exception as e:
            logging.error(e)
        for j in response1['result']['data']:
            try:
                logging.info('Get metrics')
                metrics = get_write(j['dimensions'][1]['id'] + '_' + j['dimensions'][0]['id'], response2)
            except Exception:
                metrics = None
                logging.info('No_metrics')
            try:
                if metrics is not None:
                    data_db = Data(date_and_sku=j['dimensions'][1]['id'] + '_' + j['dimensions'][0]['id'],
                                   date=datetime.datetime.strptime(j['dimensions'][1]['id'], r'%Y-%m-%d'),
                                   sku=j['dimensions'][0]['id'],
                                   sku_name=str(j['dimensions'][0]['name']),
                                   revenue=j['metrics'][0],
                                   ordered_units=j['metrics'][1],
                                   hits_view_search=j['metrics'][2],
                                   hits_view_pdp=j['metrics'][3],
                                   hits_view=j['metrics'][4],
                                   hits_tocart_search=j['metrics'][5],
                                   hits_tocart_pdp=j['metrics'][6],
                                   hits_tocart=j['metrics'][7],
                                   session_view_search=j['metrics'][8],
                                   session_view_pdp=metrics[1],
                                   session_view=metrics[2],
                                   conv_tocart_search=metrics[3],
                                   conv_tocart_pdp=metrics[4],
                                   conv_tocart=metrics[5],
                                   returns=metrics[6],
                                   cancellations=metrics[7],
                                   delivered_units=metrics[8],
                                   position_category=round(metrics[9], 3))
                else:
                    data_db = Data(date_and_sku=j['dimensions'][1]['id'] + '_' + j['dimensions'][0]['id'],
                                   date=datetime.datetime.strptime(j['dimensions'][1]['id'], r'%Y-%m-%d'),
                                   sku=j['dimensions'][0]['id'],
                                   sku_name=str(j['dimensions'][0]['name']),
                                   revenue=j['metrics'][0],
                                   ordered_units=j['metrics'][1],
                                   hits_view_search=j['metrics'][2],
                                   hits_view_pdp=j['metrics'][3],
                                   hits_view=j['metrics'][4],
                                   hits_tocart_search=j['metrics'][5],
                                   hits_tocart_pdp=j['metrics'][6],
                                   hits_tocart=j['metrics'][7],
                                   session_view_search=j['metrics'][8])
                sess.add(data_db)
                sess.commit()
                count += 1
            except Except_NoData:
                pass
            except IntegrityError as e:
                count_existing += 1
                sess.rollback()
            except OperationalError as e:
                logging.info('failed connection to the database')
                logging.info(e)
                sess.close()
                sess = create_session()
    sess.close()
    logging.info('Data import from ozon is over')
    logging.info(f'Added {count} records, existing {count_existing} records')


if __name__ == '__main__':
    logging.info('Start')
    schedule.every(2).hours.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
