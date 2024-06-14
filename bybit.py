from pybit.unified_trading import HTTP
import requests
import time
import hashlib
import hmac


def get_positions(api_key, api_secret, symbol):

    url = 'https://api.bybit.com/v5/position/list'
    params = {
        'category': 'inverse',
        'symbol': symbol
    }

    timestamp = str(int(time.time() * 1000))

    pre_sign_str = f"{timestamp}{api_key}"

    signature = hmac.new(api_secret.encode(), pre_sign_str.encode(), hashlib.sha256).hexdigest()

    headers = {
        'Content-Type': 'application/json',
        'X-BYBIT-APIKEY': api_key,
        'X-BYBIT-SIGN': signature,
        'X-BYBIT-TIMESTAMP': timestamp
    }

    response = requests.get(url, headers=headers, params=params)

    return response.json()


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


def main():

    print(get_positions("3RwoeutsTzx3lAeqWv", "QVjfIIUu35oG490lmRnzYdB0cRFLOGrWAYdK", "BTCUSDT"))


if __name__ == '__main__':
    main()
