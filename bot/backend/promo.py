from aiohttp import web
from aiohttp.web_request import Request
from bot.db import db

routes = web.RouteTableDef()


@routes.post('/promo/create')
async def create_fortune_wheel(request: Request):
    form_data = await request.json()
    print(form_data)
    ticket_name = form_data['ticket_name']
    bonus = float(form_data['bonus'])
    type_promo = int(form_data['type'])
    number_of_uses = int(form_data['number_of_uses'])
    number_of_users = int(form_data['number_of_users'])
    time_of_existence = float(form_data['time_of_existence']) * 3600 * 24
    time_of_duration = float(form_data['time_of_duration']) * 3600 * 24
    min_wager = float(form_data['min_wager'])
    wager = float(form_data['wager'])
    special_users = form_data['special_users']

    type_promo = "balance" if type_promo == 1 else 'ticket'
    number_of_users = float("Infinity") if number_of_users == 0 else number_of_users
    special_users = None if special_users == "" else special_users

    await db.add_new_promo_code(ticket_name, type_promo, bonus, time_of_duration, min_wager=min_wager, wager=wager,
                                number_of_users=number_of_users, max_deposits=number_of_uses,
                                existence_promo=time_of_existence, special_users=special_users)

    return web.Response(text='{"ok": "ok"}')
