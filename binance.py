from datetime import datetime

import requests
import schedule
from bs4 import BeautifulSoup as bs


def update_current_price():
    # Находим: максимальная цена за последний час
    max_price = None

    last_hour_prices = []
    for dt, price in prices_history.items():
        hours_ago = datetime.now() - dt
        if hours_ago.seconds / 3600 <= 1:
            last_hour_prices.append(price)
    if len(last_hour_prices) > 0:
        max_price = max(last_hour_prices)

    # Парсим текущую цену
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

    response = requests.get('https://www.binance.com/ru/markets/futures', headers=headers)
    soup = bs(response.text, 'html.parser')
    market_trade_list = soup.find_all('div', id='market_trade_list_item')
    now_price = None
    for elm in market_trade_list:
        if 'XRPUSDT' in elm.text:
            now_price = float(elm.find('div', class_='css-18cwbk1').text.replace(',', '.'))
            prices_history[datetime.now()] = now_price
            break

    # Сравниваем макс цену и текущую цену
    # if 100 - (now_price * 100 / max_price) >= 1:
    if max_price is not None and (max_price - now_price) >= max_price * 0.01:
        print('Изменилась цена на 1% или более!')
    print(f'{datetime.now().strftime("%H:%M:%S")} Макс цена за прошлый период: {max_price} Текущая цена: {now_price}')


if __name__ == '__main__':
    prices_history = {}
    schedule.every(1).seconds.do(update_current_price)

    while True:
        schedule.run_pending()
