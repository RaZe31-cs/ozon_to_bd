import requests
from data.config import Client_Id, Apikey, token_tg_bot
import logging
import time
from aiogram import Bot
import asyncio
import pandas as pd
import transliterate
import schedule
import pytz

logging.basicConfig(format='%(asctime)s;%(levelname)s;%(message)s', level=logging.INFO, filename='root/log/app8.log',
                    filemode='w')


def get_code():
    url = 'https://api-seller.ozon.ru/v1/report/discounted/create'
    headers = {
        'Content-Type': 'application/json',
        'Client-Id': Client_Id,
        'Api-Key': Apikey
    }
    r = requests.post(url, headers=headers)
    return r.json()['result']['code']


def get_data():
    try:
        code = get_code()
        logging.info(f'Get Successfully code {code}')
    except:
        logging.info('Error get code')
        return
    url = f'https://api-seller.ozon.ru/v1/report/info'
    headers = {
        'Content-Type': 'application/json',
        'Client-Id': Client_Id,
        'Api-Key': Apikey
    }
    params_json = {
        'code': code
    }
    r = requests.post(url, headers=headers, json=params_json)
    count = 0
    while r.json()['result']['status'] != 'success':
        time.sleep(5)
        r = requests.post(url, headers=headers, json=params_json)
        count += 1
        if count > 20:
            logging.info('Error get data' + r['result']['error'])
            return
    return r.json()


async def get_link(skuname):
    skuname_formed = ''
    for i in skuname:
        try:
            int(i)
        except Exception:
            if i == '/':
                skuname_formed += '-'
            else:
                skuname_formed += i
    return transliterate.translit(skuname_formed, 'ru', reversed=True)


async def send_message():
    data = get_data()
    MY_EXCEL_URL = data['result']['file']
    xl_df = pd.read_excel(MY_EXCEL_URL,
                          sheet_name='Products')
    dict_items = xl_df.to_dict()
    text = ''
    count = len(dict_items['Артикул'])
    text += f'Количество: {count}' + '\n'
    for i in range(count):
        if i != 0:
            text += '\n-----------------\n'
        """
        skuname:
        количество:
        ссылка
        """
        text += f'{dict_items["Артикул"][i]}' + '\n'
        text += f'https://www.ozon.ru/product/{await get_link(dict_items["Артикул"][i]) + str(dict_items["FBO OZON SKU ID"][i])}' + '/' + '\n'
    bot = Bot(token=token_tg_bot)
    await bot.send_message(chat_id=-1002016562525, message_thread_id=20, text=text)
    await bot.close()
    logging.info('Message send successfully' + f'{count} items')


def main():
    logging.info('Start func send_message')
    asyncio.run(send_message())


if __name__ == '__main__':
    logging.info('Start')
    schedule.every().day.at("10:00", tz=pytz.timezone('Europe/Moscow')).do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
