import asyncio
import json
import logging
import random
from datetime import datetime

from bot.db import db
from bot.consts.const import WOF_MAX_NUM, WOF_MIN_NUM
from bot.utils.rounding import round_down


async def start_wheel_of_fortune():
    logging.info('Starting Wheel of Fortune')

    wof_info = await db.get_active_wheel_info()
    sold_tickets = list(await db.get_all_sold_tickets_num())
    bank = len(sold_tickets) * wof_info.ticket_cost * wof_info.commission / 100

    random.seed(wof_info.random_seed)
    winner_num = random.randint(WOF_MIN_NUM, WOF_MAX_NUM)
    rewards = json.loads(wof_info.rewards)
    winners = await detect_winners(winner_num, sold_tickets, len(rewards))

    wof_result = await send_rewards(winners, bank, rewards)
    await db.update_wof_result(json.dumps(wof_result))


async def detect_winners(winner_num, sold_tickets, winners_count):
    # Calculate and print the scores for the participant tickets
    scores = [(ticket, score(ticket, winner_num)) for ticket in sold_tickets]

    # Find and print the winner
    winners = sorted(scores, key=lambda x: x[1])
    winners = [x[0] for x in winners[:winners_count]]
    return winners


def score(user_number, winning_number):
    # Convert numbers to strings for easy digit access
    user_number = str(user_number).zfill(7)
    winning_number = str(winning_number).zfill(7)

    # Initialize score and breakdown string
    score = 0

    # Compare each digit
    for i in range(7):
        user_digit = int(user_number[i])
        winning_digit = int(winning_number[i])

        # Add a large penalty to the score if the digits don't exactly match
        if user_digit != winning_digit:
            score_difference = abs(winning_digit - user_digit)

            # If user_digit is larger, subtract a small value to prioritize it
            score_difference -= 0.1 if user_digit > winning_digit else 0
            score_component = score_difference * 10 ** (6 - i)
            score += score_component

            # # Add a fixed large penalty to the score if the digits are not the same
            score += 1111111

    return score


async def send_rewards(winners, bank, rewards):
    wof_result = {}

    for winner_num, percent_reward in zip(winners, rewards):
        tg_id, reward = await send_reward(bank, percent_reward, winner_num)
        wof_result[winner_num] = str(tg_id) + ':' + str(reward)
    return wof_result


async def send_reward(bank, percent_reward, winner_num):
    tg_id = await db.whose_ticket(winner_num)
    reward = round_down(bank * percent_reward / 100, 2)
    await db.update_user_wof_win(tg_id, reward)
    return tg_id, reward


if __name__ == '__main__':
    asyncio.run(start_wheel_of_fortune())
