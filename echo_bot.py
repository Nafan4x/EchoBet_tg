import asyncio
from time import time, sleep

import bybit
from data import get_active_bots, update_bots


async def trade_cycle():
    while True:
        try:
            bots_list = get_active_bots()

            pended = 0
            chunk = 45
            tasks = []
            temp_l = len(bots_list)
            for bot in bots_list:
                if bot['bourse'] == 'bybit':
                    start_time = time()
                    tasks.append(asyncio.create_task(bybit.get_positions(bot)))
                    pended += 1
                    if pended % chunk == 0 or pended == temp_l:
                        for future in asyncio.as_completed(tasks):
                            temp_bot, result = await future

                            for position in result:
                                if position['side'] == temp_bot['side']:
                                    update_bots(temp_bot['bot_id'], status='active')
                                    qty = bybit.get_qty(temp_bot['base_key'], temp_bot['secret_key'],
                                                        temp_bot['symbol'], temp_bot['size'], temp_bot['reinvestment'],
                                                        float(position['leverage']))
                                    if bybit.place_order(temp_bot['base_key'], temp_bot['secret_key'],
                                                         temp_bot['symbol'], qty):
                                        update_bots(temp_bot['bot_id'], status='waiting')
                                    update_bots(temp_bot['bot_id'], status='waiting')
                                    break
                        tasks = []
                        print(time() - start_time, ' seconds', chunk - pended % chunk)

        except Exception as exept:
            print(exept)
            sleep(3)


if __name__ == '__main__':
    asyncio.run(trade_cycle())
