from data import get_active_bots, update_bots

from pybit.unified_trading import HTTP
import requests

from time import time, sleep


def trade_cycle():
    while True:
        try:
            start_time = time()
            bots_list = get_active_bots()
            base_key = ''
            for bot in bots_list:
                if base_key != bot['base_key']:
                    session = HTTP(
                        api_key=bot['base_key'],
                        api_secret=bot['secret_key'],
                    )
                    base_key = bot['base_key']
                try:
                    positions = session.get_positions(
                        category="linear",
                        symbol=bot['symbol'],
                    )
                except requests.exceptions.ReadTimeout:
                    print("Request timed out. Retrying...")
                    continue
                except requests.exceptions.RequestException as e:
                    print(f"Request failed: {e}")
                    continue

                for position in positions['result']['list']:
                    if position['side'] == bot['side']:
                        update_bots(bot['bot_id'], status='active')
                        break
            print(time() - start_time, ' seconds')
            sleep(1000)
        except Exception as exept:
            print(exept)


if __name__ == '__main__':
    trade_cycle()
