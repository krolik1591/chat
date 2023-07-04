import time

from bot.db.models import User, WoFSettings, WoFTickets


async def add_wheel_of_fortune_settings(ticket_cost, commission, rewards, random_seed, date_end=None):
    return await WoFSettings.create(ticket_cost=ticket_cost, commission=commission, rewards=rewards,
                                    timestamp_end=date_end, timestamp_start=time.time(), random_seed=random_seed)


async def add_new_ticket(user_id, tickets_num, ticket_type, buy_timestamp=time.time()):
    ticket_objects = [
        WoFTickets(user_id=user_id, ticket_num=ticket_num, ticket_type=ticket_type,
                   buy_timestamp=buy_timestamp)
        for ticket_num in tickets_num
    ]
    await WoFTickets.bulk_create(ticket_objects)


async def get_active_wheel_info():
    result = await WoFSettings.select().where(WoFSettings.is_active == 1)
    if len(result) == 0:
        return None
    return result[0]


async def get_last_deactivate_wheel_info():
    result = await WoFSettings.select().where(WoFSettings.is_active == 0).order_by(WoFSettings.timestamp_end.desc())
    if len(result) == 0:
        return None
    return result[0]


async def get_count_user_tickets(tg_id, type_):
    if type_ == 'all':
        result = await WoFTickets.select().where(WoFTickets.user_id == tg_id).count()
    else:
        result = await WoFTickets.select().where(WoFTickets.user_id == tg_id, WoFTickets.ticket_type == type_).count()
    return result


async def get_user_ticket_numbers(tg_id, type_, offset=0, limit=100):
    if type_ == 'all':
        result = await WoFTickets.select(WoFTickets.ticket_num) \
            .where(WoFTickets.user_id == tg_id) \
            .offset(offset).limit(limit)
    else:
        result = await WoFTickets.select(WoFTickets.ticket_num) \
            .where(WoFTickets.user_id == tg_id, WoFTickets.ticket_type == type_) \
            .offset(offset).limit(limit)

    tickets = [ticket.ticket_num for ticket in result]
    return tickets


async def get_user_wof_win(tg_id):
    result = await User.select(User.wof_win).where(User.user_id == tg_id)
    return result[0].wof_win  # todo why fetch all and return only first? why first?


async def get_all_sold_tickets_nums():
    result = await WoFTickets.select(WoFTickets.ticket_num)
    return set(ticket.ticket_num for ticket in result)


async def get_user_id_wof_participants():
    result = await WoFTickets.select(WoFTickets.user_id).distinct()
    return set(user.user_id for user in result)


async def get_all_tickets():
    return await WoFTickets.select()


async def check_ticket_in_db(ticket_num):
    result = await WoFTickets.select().where(WoFTickets.ticket_num == ticket_num)
    if len(result) == 0:
        return False
    return True


async def update_user_wof_win(tg_id, win):
    if win == 0:
        return await User.update({User.wof_win: 0}).where(User.user_id == tg_id)
    return await User.update({User.wof_win: User.wof_win + win}).where(User.user_id == tg_id)


async def whose_ticket(ticket_num):
    result = await WoFTickets.select().where(WoFTickets.ticket_num == ticket_num)
    return result[0].user_id


async def update_wof_result(winners):
    return await WoFSettings.update({WoFSettings.is_active: 0, WoFSettings.winners: winners}) \
        .where(WoFSettings.is_active == 1)


async def delete_wof_tickets():
    return await WoFTickets.delete()


async def change_date_end(date_end):
    return await WoFSettings.update({WoFSettings.timestamp_end: date_end}).where(WoFSettings.is_active == 1)


if __name__ == '__main__':
    async def test():
        x = await get_user_id_wof_participants()
        print(x)


    import asyncio

    asyncio.run(test())
