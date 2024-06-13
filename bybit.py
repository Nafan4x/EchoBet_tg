from pybit.unified_trading import HTTP
import requests


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
    trading_pairs = get_trading_pairs('BTCUSDT')
    print(trading_pairs)


if __name__ == '__main__':
    main()
