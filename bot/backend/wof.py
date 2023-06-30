import json
import random
import secrets
import time

from aiohttp import web
from aiohttp.web_request import Request

from bot.cron.wof_watcher import display_winners_info, get_winner_tickets
from bot.db import db

routes = web.RouteTableDef()


@routes.get('/wof/get')
async def get_fortune_wheel(request: Request):
    wheel = await db.get_active_wheel_info()
    if not wheel:
        return web.Response(text="null")

    winners_info = await display_winners_info(wheel)

    winner_tickets = get_winner_tickets(wheel.random_seed, len(wheel.rewards))

    tickets = await db.get_all_tickets()
    result = {
        'wheel': wheel.__data__,
        'tickets': [t.__data__ for t in tickets],
        'winners_info': winners_info,
        'winner_tickets': winner_tickets
    }

    return web.json_response(text=json.dumps(result, default=str))


@routes.post('/wof/add_win_ticket')
async def add_win_ticket(request: Request):
    form_data = await request.json()
    print(form_data)
    try:
        ticket_number = int(form_data['ticket_number'])
    except ValueError as e:
        return web.Response(text='{"error": "ticket_number is not int"}')

    if await db.check_ticket_in_db(ticket_number):
        return web.Response(text='{"error": "ticket_number is already exists"}')

    await db.add_new_ticket(form_data['admin_id'], [ticket_number],
                            'random', time.time() + random.randint(172800, 1209600))

    return web.Response(text='{"ok": "ok"}')


@routes.post('/wof/change_date_end')
async def add_win_ticket(request: Request):
    form_data = await request.json()
    await db.change_date_end(form_data['end_date'])
    return web.Response(text='{"ok": "ok"}')


@routes.post('/wof/create')
async def create_fortune_wheel(request: Request):
    form_data = await request.json()
    print(form_data)
    try:
        ticket_cost = int(form_data['ticket_cost'])
        commission = int(form_data['commission'])
        date_end = int(form_data['end_date'])
        winner_list = json.dumps(form_data['distribution'])
        nonce = secrets.token_bytes(16).hex()  # generate a 16-byte (128-bit)
        await db.add_wheel_of_fortune_settings(ticket_cost, commission, winner_list, nonce, date_end)

    except Exception as e:
        return web.Response(text=f"Error: {e}", status=400)
    return web.Response(text='{"ok": "ok"}')
