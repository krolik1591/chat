import hashlib
import hmac
import json
import time
from urllib.parse import unquote

import aiohttp_cors
from aiohttp import web
from aiohttp.web_request import Request

from bot.db.methods import add_wheel_of_fortune_settings
from bot.utils.cert import get_ssl_context

routes = web.RouteTableDef()


@routes.get('/')
async def hello(request: Request):
    return web.Response(text="Hello, world")


@routes.get('/get_fortune_wheel')
async def is_exist_wheel(request: Request):
    assert check_auth(request.headers.get("X-Auth"), request.app['bot'].token), "Invalid auth"

    hui = {
        'ticket_cost': 10,
        'date_creature': '2021-10-10',
        'date_end': '2021-10-11',
    }
    # return web.Response(text=json.dumps(hui))
    return web.json_response(text='false')


@routes.post('/create_fortune_wheel')
async def create_fortune_wheel(request: Request):
    assert check_auth(request.headers.get("X-Auth"), request.app['bot'].token), "Invalid auth"

    form_data = await request.json()
    try:
        ticket_cost = int(form_data['ticket_cost'])
    except ValueError:
        return web.Response(text='"Ticket cost must be a number"', status=400)

    date_end = form_data['end_date']
    if date_end < time.time():
        return web.Response(text='"Date end must be in the future"')

    winner_list = json.dumps(form_data['distribution'])
    await add_wheel_of_fortune_settings(ticket_cost, form_data['commission'], winner_list, form_data['end_date'])
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

    web.run_app(app, port=port, ssl_context=ssl_context)
    web.run_app(app, port=port, loop=loop)


if __name__ == "__main__":
    from aiogram import Bot
    from bot.utils.config_reader import config
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    run(bot=bot, ssl_context=get_ssl_context("0.0.0.0"))
