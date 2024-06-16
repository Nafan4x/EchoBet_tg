import asyncio
import hashlib
import hmac
import time

import aiohttp
import requests
from pybit.unified_trading import HTTP

from bybit_lot_size_info import lot_size_info


async def get_positions(bot):
    api_key = bot['base_key']
    api_secret = bot['secret_key']
    symbol = bot['symbol']
    timestamp = str(int(time.time() * 1000))
    recv_window = '5000'
    queryString = f'category=linear&symbol={symbol}'

    param_str = f"{timestamp}{api_key}{recv_window}{queryString}"

    sign = hmac.new(
        bytes(api_secret, 'utf-8'),
        bytes(param_str, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    url = f"https://api.bybit.com/v5/position/list?{queryString}"

    headers = {
        'X-BAPI-SIGN': sign,
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-TIMESTAMP': timestamp,
        'X-BAPI-RECV-WINDOW': recv_window,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response_data = await response.json()
            return bot, response_data['result']['list']


def get_lot_size():
    arr = get_trading_info()
    if arr is None:
        return False
    return [(item['name'], item['lot_size_filter'],) for item in arr]


def get_trading_info():
    url = "https://api.bybit.com/v2/public/symbols"
    response = requests.get(url)
    data = response.json()
    if data['ret_code'] == 0:
        return data['result']
    else:
        print("Error fetching trading pairs:", data['ret_msg'])
        return


def get_qty(api_key, api_secret, symbol, trading_sum, reinvestment, leverage):
    try:
        url = 'https://api.bybit.com/derivatives/v3/public/order-book/L2'
        params = {
            'category': 'linear',
            'symbol': symbol,
            'limit': 1,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            last_price = round((float(data['result']['a'][0][0]) + float(data['result']['b'][0][0])) / 2,
                               lot_size_info[symbol]['price_scale'])
            session = HTTP(
                api_key=api_key,
                api_secret=api_secret,
            )
            curr_balance = float(session.get_wallet_balance(
                accountType="UNIFIED",
                coin="USDT",
            )['result']['list'][0]['totalMarginBalance'])
            step = lot_size_info[symbol]['lot_size_filter']['qty_step']
            if curr_balance >= trading_sum:
                qtyForBuy = (trading_sum * leverage / last_price) // step * step
                if qtyForBuy > 0:
                    return qtyForBuy
            elif reinvestment > 0:
                qtyForBuy = (curr_balance * 0.98 * leverage / last_price) // step * step
                if qtyForBuy > 0:
                    return qtyForBuy
            return None
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code}")
    except Exception as exept:
        print(exept)
        return


def place_order(api_key, api_secret, symbol, qtyForBuy):
    try:
        session = HTTP(
            api_key=api_key,
            api_secret=api_secret,
        )
        order_response = session.place_order(
            category="linear",
            symbol=symbol,
            side="Buy",
            orderType="Market",
            qty=f"{qtyForBuy}",
            positionIdx="1",
        )
        print('Order placed:', order_response)
        return False
    except requests.exceptions.ReadTimeout:
        print("Request timed out. Retrying...")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return True


def get_trading_pairs(symbol):
    arr = get_trading_info()
    if arr is None:
        return False
    return symbol.upper() in [item['name'] for item in arr]


def check_session(api_key, api_secret):
    try:
        session = HTTP(
            api_key=api_key,
            api_secret=api_secret,
        )
        positions = session.get_positions(
            category="linear",
            symbol='BTCUSDT',
        )
        return True
    except Exception as exept:
        print(exept)
        return False


async def main():
    api_key = "3RwoeutsTzx3lAeqWv"
    api_secret = "QVjfIIUu35oG490lmRnzYdB0cRFLOGrWAYdK"
    symbol = "1000PEPEUSDT"
    # get_last_price(symbol)
    print(get_qty(api_key, api_secret, symbol, 16800, 0.1, 10))


if __name__ == '__main__':
    asyncio.run(main())
