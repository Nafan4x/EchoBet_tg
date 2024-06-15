from pybit.unified_trading import HTTP
import requests
import time
import hashlib
import hmac
import aiohttp
import asyncio


async def get_positions(api_key, api_secret, symbol, index, side):
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
            return index, side, response_data['result']['list']


def get_trading_pairs(symbol):
    url = "https://api.bybit.com/v2/public/symbols"
    response = requests.get(url)
    data = response.json()

    if data['ret_code'] == 0:
        trading_pairs = [item['name'] for item in data['result']]
        return symbol.upper() in trading_pairs
    else:
        print("Error fetching trading pairs:", data['ret_msg'])
        return False


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
    start_time = time.time()
    api_key = "3RwoeutsTzx3lAeqWv"
    api_secret = "QVjfIIUu35oG490lmRnzYdB0cRFLOGrWAYdK"
    symbol = "1000PEPEUSDT"

    tasks = [get_positions(api_key, api_secret, symbol, _) for _ in range(50)]
    for future in asyncio.as_completed(tasks):
        index, result = await future
        print(f"Response from task {index}: {result}")

    print(time.time() - start_time, ' seconds')

if __name__ == '__main__':
    asyncio.run(main())
