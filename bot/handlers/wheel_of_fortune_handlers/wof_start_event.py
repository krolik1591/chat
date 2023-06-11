import asyncio
import json
import random
from datetime import datetime

from bot.db import db
from bot.consts.const import WOF_MAX_NUM, WOF_MIN_NUM
from bot.utils.rounding import round_down


async def start_wof_timer(date_end):
    now = datetime.utcnow()
    time_delta = date_end - now
    seconds = time_delta.total_seconds()
    asyncio.create_task(asyncio.sleep(seconds, start_wheel_of_fortune()))


async def start_wheel_of_fortune():
    wof_info = await db.get_active_wheel_info()
    sold_tickets = list(await db.get_all_sold_tickets_num())
    bank = len(sold_tickets) * wof_info.ticket_price

    winner_num = random.randint(WOF_MIN_NUM, WOF_MAX_NUM)
    rewards_and_winners = json.loads(wof_info.rewards)
    winners = await detect_winners(winner_num, rewards_and_winners, sold_tickets)
    await send_rewards(winners, bank)


async def send_rewards(winners, bank):
    for winner_num, percent_reward in winners.items():
        tg_id = await db.whose_ticket(winner_num)
        reward = round_down(bank * percent_reward / 100, 2)
        await db.update_user_wof_win(tg_id, reward)


async def detect_winners(winner_num, rewards_and_winners, sold_tickets):
    winners = {}
    sorted_numbers = sorted(sold_tickets, key=lambda x: abs(x - (winner_num - 0.1)))
    winner_numbers = sorted_numbers[:len(rewards_and_winners)]
    for i in range(len(winner_numbers)):
        winners[int(winner_numbers[i] + 0.1)] = rewards_and_winners[i]
    return winners


if __name__ == '__main__':
    asyncio.run(start_wheel_of_fortune())
