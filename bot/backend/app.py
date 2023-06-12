import hashlib
import hmac
import json
import secrets
from urllib.parse import unquote

import aiohttp_cors
from aiohttp import web
from aiohttp.web_request import Request

from bot.db import db
from bot.handlers.wheel_of_fortune_handlers.buy_ticket import buy_winner_tickets
from bot.utils.cert import get_ssl_context

routes = web.RouteTableDef()


@routes.get('/')
async def hello(request: Request):
    return web.Response(text="Hello, world")


@routes.get('/get_fortune_wheel')
async def get_fortune_wheel(request: Request):
    assert check_auth(request.headers.get("X-Auth"), request.app['bot'].token), "Invalid auth"
    wheel = await db.get_active_wheel_info()
    if not wheel:
        return web.Response(text="null")

    tickets = await db.get_all_tickets()
    result = {
        'wheel': wheel.__data__,
        'tickets': [t.__data__ for t in tickets]
    }

    return web.json_response(text=json.dumps(result, default=str))


@routes.post('/create_fortune_wheel')
async def create_fortune_wheel(request: Request):
    assert check_auth(request.headers.get("X-Auth"), request.app['bot'].token), "Invalid auth"

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
            await buy_winner_tickets(admin_id, winner_tickets_count, nonce)

    except Exception as e:
        return web.Response(text=f"Error: {e}", status=400)
    return web.Response(text='{"ok": "ok"}')


# todo as middleware
def check_auth(auth: str, bot_token: str):
    bot_token = hashlib.sha256(bot_token.encode()).digest()

    auth = json.loads(unquote(auth))
    token = "\n".join(sorted([f"{k}={v}" for k, v in auth.items() if k != "hash"]))
    token_hash = hmac.new(bot_token, token.encode(), hashlib.sha256).hexdigest()

    return auth["hash"] == token_hash


def run(port=8080, loop=None, bot=None, ssl_context=None):
    app = web.Application()
    app['bot'] = bot
    app.add_routes(routes)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*")
    })
    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(app, port=port, loop=loop, ssl_context=ssl_context)


if __name__ == "__main__":
    from aiogram import Bot
    from bot.utils.config_reader import config
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    run(bot=bot, ssl_context=get_ssl_context("0.0.0.0"))
