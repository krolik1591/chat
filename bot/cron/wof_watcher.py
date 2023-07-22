import asyncio
import json
import logging
import random
import time
from asyncio import sleep

from aiogram import exceptions
from aiogram.utils.i18n import gettext as _

from bot.consts.const import WOF_MAX_NUM, WOF_MIN_NUM
from bot.db import db, manager
from bot.menus.utils import kb_del_msg_for_spam
from bot.tokens.token_ton.tx_watcher import set_user_locale_to_i18n
from bot.utils.rounding import round_down

HOUR = 120


async def start_wof_timer(bot, i18n):
    await spin_wheel_of_fortune(bot, i18n)

    while True:
        logging.info("WOF TIMER STARTED")
        wof_info = await db.get_active_wheel_info()

        if not wof_info:
            await asyncio.sleep(HOUR)
            logging.info("WOF TIMER SLEEP")
            continue

        if not wof_info.timestamp_end:
            await asyncio.sleep(HOUR)
            logging.info("WOF TIMER SLEEP")
            continue

        time_before_wof_finish = wof_info.timestamp_end - time.time()
        logging.info(f"Seconds to WOF: {time_before_wof_finish}")
        if time_before_wof_finish < HOUR:
            await asyncio.sleep(time_before_wof_finish)
            logging.info("Timer to WOF is started")
            await spin_wheel_of_fortune(bot, i18n)

        await asyncio.sleep(HOUR)


async def spin_wheel_of_fortune(bot, i18n):
    logging.info('Starting Wheel of Fortune')
    print('Starting Wheel of Fortune')

    wof_info = await db.get_active_wheel_info()
    sold_tickets = list(await db.get_all_sold_tickets_nums())
    bank = len(sold_tickets) * wof_info.ticket_cost * (100 - wof_info.commission) / 100
    rewards = json.loads(wof_info.rewards)

    win_tickets = get_winner_tickets(wof_info.random_seed, len(rewards))

    numbers_won = []
    winners = [
        detect_winner(win_ticket, sold_tickets, numbers_won)
        for win_ticket in win_tickets
    ]
    winners = [winner for winner in winners if winner is not None]

    winners_info = []
    for winner_num, percent_reward in zip(winners, rewards):
        tg_id = await db.whose_ticket(winner_num)
        reward = round_down(bank * percent_reward / 100, 2)
        print(f'Winner: {tg_id}, num: {winner_num}, reward: {reward}')
        winners_info.append((winner_num, tg_id, reward))

        won_json = await db.get_user_wof_win(tg_id)
        won = json.loads(won_json)

        promo_name = await db.ticket_is_promo(winner_num)
        if promo_name:
            won['promo'] = won['promo'] + reward
            await db.update_won_condition(tg_id, promo_name)
        else:
            won['general'] = won['general'] + reward

        await db.update_user_wof_win(tg_id, json.dumps(won))

    with manager.pw_database.atomic():
        await deactivate_users_promo_codes()
        await db.update_wof_result(json.dumps(winners_info))
        await db.delete_wof_tickets()

    await send_msg_to_wof_participants(bot, winners_info, i18n)


async def deactivate_users_promo_codes():
    unique_promo_codes = await db.get_unique_promocode_from_wof_tickets()
    for promo_name in unique_promo_codes:
        unique_users = await db.get_unique_users_by_promo_code(promo_name)
        for user_id in unique_users:
            if await db.can_deactivate_ticket_promo(user_id, promo_name):
                await db.deactivate_user_promo_code(user_id, promo_name)


def get_winner_tickets(seed, count=1):
    random.seed(seed)
    return [
        random.randint(WOF_MIN_NUM, WOF_MAX_NUM)
        for _ in range(count)
    ]


def detect_winner(winner_num, sold_tickets, number_won):
    sold_tickets_without_winners = list(set(sold_tickets) - set(number_won))
    if not sold_tickets_without_winners:
        return None

    scores = (
        (ticket, calc_score(ticket, winner_num))
        for ticket in sold_tickets_without_winners
    )
    winner = min(scores, key=lambda x: x[1])
    number_won.append(winner[0])
    return winner[0]


def calc_score(user_number, winning_number):
    user_number = str(user_number).zfill(7)
    winning_number = str(winning_number).zfill(7)

    score = 0  # actually penalty

    for digit in range(7):
        user_digit = int(user_number[digit])
        winning_digit = int(winning_number[digit])
        score += calc_score_digit(user_digit, winning_digit, 6 - digit)

    return score


def calc_score_digit(user_digit, winning_digit, digit_index):
    if user_digit == winning_digit:
        return 0

    score_difference = abs(winning_digit - user_digit)
    if user_digit > winning_digit:
        score_difference -= 0.1  # If user_digit is larger, subtract a small value to prioritize it

    score_difference *= 10 ** digit_index  # first (left) digits are more important

    return 1111111 + score_difference


async def display_winners_info(wof_info):
    rewards = json.loads(wof_info.rewards)
    win_tickets = get_winner_tickets(wof_info.random_seed, len(rewards))
    sold_tickets = list(await db.get_all_sold_tickets_nums())
    bank = len(sold_tickets) * wof_info.ticket_cost * (100 - wof_info.commission) / 100

    numbers_won = []
    winners = [
        detect_winner(win_ticket, sold_tickets, numbers_won)
        for win_ticket in win_tickets
    ]
    winners = [winner for winner in winners if winner is not None]
    if len(winners) < len(rewards):
        dif = len(rewards) - len(winners)
        for _ in range(dif):
            winners.append(0)

    winners_info = []
    for winner_num, percent_reward, win_ticket in zip(winners, rewards, win_tickets):
        if winner_num == 0:
            tg_id = 0
        else:
            tg_id = await db.whose_ticket(winner_num)
        winners_info.append((str(winner_num).zfill(7), tg_id, str(win_ticket).zfill(7), bank * percent_reward / 100))

    return winners_info


async def send_msg_to_wof_participants(bot, winners_info, i18n):
    users = await db.get_user_id_wof_participants()
    winners = set()
    for index, winner in enumerate(winners_info, start=1):
        winners.add(winner[1])
        await set_user_locale_to_i18n(winner[1], i18n)
        await send_msg(bot, winner[1], _('WOF_WATCHER_SEND_MSG_TO_WOF_WINNERS')
                       .format(winner_num=str(winner[0]).zfill(7), reward=winner[2], pos=index))

    loosers = users - winners
    for looser in loosers:
        await set_user_locale_to_i18n(looser, i18n)
        await send_msg(bot, looser, _('WOF_WATCHER_SEND_MSG_TO_WOF_LOOSERS'))


async def send_msg(bot, user_id, text):
    for i in range(5):
        try:
            await bot.send_message(user_id, text, reply_markup=kb_del_msg_for_spam())
            return None  # no errors!
        except exceptions.TelegramRetryAfter as e:
            print(f"So much messages. Need to sleep {e.retry_after} sec")
            await sleep(e.retry_after)
            continue

        except exceptions.TelegramForbiddenError:
            await db.user_blocked_bot(user_id)
            return f"{user_id} blocked the bot"

        except exceptions.TelegramBadRequest:
            return f"{user_id} doesn't exist"

    else:
        return f"{user_id} flood limit"
