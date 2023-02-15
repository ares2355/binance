import requests
from bs4 import BeautifulSoup as bs
import schedule
from datetime import datetime


def get_current_price():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

    response = requests.get('https://www.binance.com/ru/markets/futures', headers=headers)
    soup = bs(response.text, 'lxml')
    xrp_usdt = soup.find_all('div', id='market_trade_list_item')
    for i in xrp_usdt:
        if 'XRPUSDT' in i.text:
            now_price = float(i.find('div', class_='css-18cwbk1').text.replace(',', '.'))
            # history_price[now_time.strftime("%d-%m-%Y %H:%M")] = now_price
            history_price.append({now_time.strftime("%d-%m-%Y %H:%M"): now_price})
            count =+ 1
        return now_price


def get_last_price():
    if count == 59:
        get_current_price()
        last_price = history_price[-1]
        now_price = history_price[0]
        for i in last_price:
            last_price = last_price[i]
            for v in now_price:
                now_price = now_price[v]
        if 100 - (last_price * 100 / now_price) == 1:
            history_price.clear()
        else:
            return 0


if __name__ == '__main__':
    count = 0
    now_time = datetime.now()
    history_price = []
    schedule.every(1).minutes.do(get_current_price)

    while True:
        if get_last_price() != 0:
            print('Current change on 1%')
        schedule.run_pending()
# li = []
# for i in map(lambda x: x, xrp_usdt):
#     if 'XRPUSDT' in i.text:
#         li.append(i.text.strip('XRPUSDTбессрочный M–ИсторияТорговать$').split('/'))
# current_price = li[0][0]
#
# print(current_price)
