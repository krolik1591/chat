import json
import secrets

from aiohttp import web
from aiohttp.web_request import Request

from bot.cron.wof_watcher import display_winners_info
from bot.db import db
from bot.handlers.wheel_of_fortune_handlers.buy_ticket import buy_winner_tickets

routes = web.RouteTableDef()


@routes.get('/get_fortune_wheel')
async def get_fortune_wheel(request: Request):
    wheel = await db.get_active_wheel_info()
    if not wheel:
        return web.Response(text="null")

    if await db.get_all_tickets():
        winners_info = await display_winners_info(wheel)
    else:
        winners_info = [(0, 0)]

    tickets = await db.get_all_tickets()
    result = {
        'wheel': wheel.__data__,
        'tickets': [t.__data__ for t in tickets],
        'winners_info': winners_info
    }

    return web.json_response(text=json.dumps(result, default=str))


@routes.post('/add_win_ticket')
async def add_win_ticket(request: Request):
    form_data = await request.json()
    await buy_winner_tickets(form_data['admin_id'], 1)
    return web.Response(text='{"ok": "ok"}')


@routes.post('/create_fortune_wheel')
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

        winner_tickets_count = int(form_data['winner_tickets_count'])
        if winner_tickets_count > 0:
            admin_id = form_data['admin_id']
            await buy_winner_tickets(admin_id, winner_tickets_count)

    except Exception as e:
        return web.Response(text=f"Error: {e}", status=400)
    return web.Response(text='{"ok": "ok"}')
