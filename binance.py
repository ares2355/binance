import requests
from bs4 import BeautifulSoup as bs
import schedule


def f():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

    response = requests.get('https://www.binance.com/ru/markets/futures', headers=headers)
    soup = bs(response.text, 'lxml')
    xrp_usdt = soup.find_all('div', id='market_trade_list_item')
    for i in map(lambda x: x, xrp_usdt):
        if 'XRPUSDT' in i.text:
            price = float(i.find('div', class_='css-18cwbk1').text.replace(',', '.'))
    return price


def func():
    last_price = f()
    if 100 - (last_price * 100 / current_price) == 1:
        print('ok')
        return last_price
    else:
        return 0

if __name__ == '__main__':
    current_price = f()
    print(current_price)
    last = func()
    schedule.every(1).minutes.do(func)

    while True:
        if last != 0:
            current_price = last
        schedule.run_pending()

# li = []
# for i in map(lambda x: x, xrp_usdt):
#     if 'XRPUSDT' in i.text:
#         li.append(i.text.strip('XRPUSDTбессрочный M–ИсторияТорговать$').split('/'))
# current_price = li[0][0]
#
# print(current_price)
