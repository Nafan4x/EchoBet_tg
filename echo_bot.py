from EchoBet_tg.bybit import get_positions
from data import get_active_bots, update_bots
import aiohttp
import asyncio
from pybit.unified_trading import HTTP
import requests
from time import time, sleep


async def trade_cycle():
    while True:
        try:
            bots_list = get_active_bots()

            pended = 0
            chunk = 45
            tasks = []
            temp_l = len(bots_list)
            for bot in bots_list:
                start_time = time()
                tasks.append(asyncio.create_task(get_positions(bot['base_key'], bot['secret_key'], bot['symbol'], bot['bot_id'], bot['side'])))
                pended += 1
                if pended % chunk == 0 or pended == temp_l:
                    for future in asyncio.as_completed(tasks):
                        index, side, result = await future

                        for position in result:
                            if position['side'] == side:
                                update_bots(index, status='active')
                                break
                    tasks = []
                    print(time() - start_time, ' seconds', chunk)

        except Exception as exept:
            print(exept)


if __name__ == '__main__':
    asyncio.run(trade_cycle())
