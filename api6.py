import requests
import schedule
from data.config import Apikey, Client_Id
import logging
import json
import datetime
from data.db_session import global_init, create_session
from data.models.data6 import Data6
from data.models.data6_delivery import Data6Delivery
from data.models.data6_others import Data6Others
from data.models.data6_payments import Data6Payments
from data.models.data6_cash_flows import Data6CashFlows
from data.models.data6_services import Data6Service
from data.models.data6_return_services import Data6ReturnService
import time

logging.basicConfig(format='%(asctime)s;%(levelname)s;%(message)s', level=logging.INFO, filename='root/log/app6.log',
                    filemode='w')


def get_data():
    headers = {
        "Client-Id": Client_Id,
        "Api-Key": Apikey
    }
    params = {
        "date": {
            "from": f"{(datetime.datetime.now() - datetime.timedelta(days=14)).strftime('%Y-%m-%d')}T00:00:00.000Z",
            "to": f"{datetime.datetime.now().strftime('%Y-%m-%d')}T00:00:00.000Z"
        },
        "with_details": True,
        "page": 1,
        "page_size": 1000
    }
    logging.info(
        f'GET DATA from {params["date"]["from"]} to {params["date"]["to"]}, page {params["page"]}, page_size {params["page_size"]}')
    response = requests.post("https://api-seller.ozon.ru/v1/finance/cash-flow-statement/list", headers=headers,
                             json=params)
    if response:
        data = response.json()
        return data
    return False


def delete_old_data(sess, data6):
    data6_cash_flows_list = sess.query(Data6CashFlows).filter(
        Data6CashFlows.id_v1_finance_cash_flow_statement_list == data6.id).all()
    data6_delivery_list = sess.query(Data6Delivery).filter(
        Data6Delivery.id_v1_finance_cash_flow_statement_list == data6.id).all()
    data6_others_list = sess.query(Data6Others).filter(
        Data6Others.id_v1_finance_cash_flow_statement_list == data6.id).all()
    data6_payments_list = sess.query(Data6Payments).filter(
        Data6Payments.id_v1_finance_cash_flow_statement_list == data6.id).all()
    data6_services_list = sess.query(Data6Service).filter(
        Data6Service.id_v1_finance_cash_flow_statement_list == data6.id).all()
    data6_return_services_list = sess.query(Data6ReturnService).filter(
        Data6ReturnService.id_v1_finance_cash_flow_statement_list == data6.id).all()
    for i in data6_cash_flows_list:
        sess.delete(i)
    for i in data6_delivery_list:
        sess.delete(i)
    for i in data6_others_list:
        sess.delete(i)
    for i in data6_payments_list:
        sess.delete(i)
    for i in data6_services_list:
        sess.delete(i)
    for i in data6_return_services_list:
        sess.delete(i)
    sess.delete(data6)
    sess.commit()


def load_in_db(data):
    try:
        logging.info('Connect with database')
        global_init('finance')
        sess = create_session()
        logging.info('successfully connect')
    except Exception as e:
        logging.error('Error connect with database')
        raise e
    for i, j in zip(data['result']['cash_flows'], data['result']['details']):
        old_data = sess.query(Data6).filter(Data6.period_id == int(j['period']['id'])).first()
        if old_data is not None:
            logging.info('find date -- update....')
            delete_old_data(sess, old_data)
            logging.info('successfully update')
        data = Data6(period_begin=j['period']['begin'],
                     period_end=j['period']['end'],
                     period_id=int(j['period']['id']),
                     begin_balance_amount=float(j['begin_balance_amount']),
                     delivery_total=float(j['delivery']['total']),
                     delivery_amount=float(j['delivery']['amount']),
                     delivery_services_total=j['delivery']['delivery_services']['total'],
                     return_total=float(j['return']['total']),
                     return_amount=float(j['return']['amount']),
                     return_services_total=float(j['return']['return_services']['total']),
                     loan=float(j['loan']),
                     invoice_transfer=float(j['invoice_transfer']),
                     rfbs_total=float(j['rfbs']['total']),
                     rfbs_transfer_delivery=float(j['rfbs']['transfer_delivery']),
                     rfbs_transfer_delivery_return=float(j['rfbs']['transfer_delivery_return']),
                     rfbs_compensation_delivery_return=float(j['rfbs']['compensation_delivery_return']),
                     rfbs_partial_compensation=float(j['rfbs']['partial_compensation']),
                     rfbs_partial_compensation_return=float(j['rfbs']['partial_compensation_return']),
                     others_total=float(j['others']['total']),
                     end_balance_amount=float(j['end_balance_amount']))
        sess.add(data)
        sess.flush()
        data_CashFlows = Data6CashFlows(id_v1_finance_cash_flow_statement_list=data.id,
                                        commission_amount=float(i['commission_amount']),
                                        currency_code=i['currency_code'],
                                        item_delivery_and_return_amount=float(i['item_delivery_and_return_amount']),
                                        orders_amount=float(i['orders_amount']),
                                        period_begin=i['period']['begin'],
                                        period_end=i['period']['end'],
                                        period_id=int(i['period']['id'])
                                        )
        sess.add(data_CashFlows)
        for item in j['services']['items']:
            data_service = Data6Service(id_v1_finance_cash_flow_statement_list=data.id,
                                        name=item['name'],
                                        price=float(item['price']))
            sess.add(data_service)
        for item in j['others']['items']:
            data_other = Data6Others(id_v1_finance_cash_flow_statement_list=data.id,
                                     name=item['name'],
                                     price=float(item['price']))
            sess.add(data_other)
        for item in j['payments']:
            data_payment = Data6Payments(id_v1_finance_cash_flow_statement_list=data.id,
                                         payment=float(item['payment']),
                                         currency_code=item['currency_code'])
            sess.add(data_payment)
        for item in j['delivery']['delivery_services']['items']:
            data_delivery = Data6Delivery(id_v1_finance_cash_flow_statement_list=data.id,
                                          name=item['name'],
                                          price=float(item['price']))
            sess.add(data_delivery)
        for item in j['return']['return_services']['items']:
            data_return_service = Data6ReturnService(id_v1_finance_cash_flow_statement_list=data.id,
                                                     name=item['name'],
                                                     price=float(item['price']))
            sess.add(data_return_service)
        try:
            logging.info('commit')
            sess.commit()
            logging.info('seccessfully commit')
        except Exception:
            logging.error('Error commit')


def main():
    data = get_data()
    if data:
        load_in_db(data)
    else:
        logging.error('Error get data')


if __name__ == '__main__':
    # main()
    logging.info('Start')
    schedule.every().day.at("09:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
