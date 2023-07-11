import hashlib
import hmac
import json
from urllib.parse import unquote

import aiohttp_cors
from aiohttp import web
from aiohttp.web import middleware
from aiohttp.web_request import Request

from bot.backend.other import routes as other_routers
from bot.backend.wof import routes as wof_routers
from bot.backend.users import routes as users_routers

from bot.utils.config_reader import config


@middleware
async def check_auth_middleware(request: Request, handler):
    if request.method != "OPTIONS":
        auth = request.headers.get("X-Auth")
        bot_token = request.app['bot'].token

        if not auth or auth == "null":
            return web.Response(text="No auth header", status=401)

        is_valid, tg_id = check_auth(auth, bot_token)
        if not is_valid:
            return web.Response(text="Invalid auth", status=401)
        if str(tg_id) not in config.admin_ids:
            return web.Response(text="Not a admin", status=401)

    return await handler(request)


# todo as middleware
def check_auth(auth: str, bot_token: str):
    bot_token = hashlib.sha256(bot_token.encode()).digest()
    auth = json.loads(unquote(auth))
    token = "\n".join(sorted([f"{k}={v}" for k, v in auth.items() if k != "hash"]))
    token_hash = hmac.new(bot_token, token.encode(), hashlib.sha256).hexdigest()

    return auth["hash"] == token_hash, auth["id"]


def run(port=8080, loop=None, bot=None, ssl_context=None):
    app = web.Application(middlewares=[check_auth_middleware])
    app['bot'] = bot
    app.add_routes(wof_routers)
    app.add_routes(other_routers)
    app.add_routes(users_routers)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*")
    })
    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(app, port=port, loop=loop, ssl_context=ssl_context)


# if __name__ == "__main__":
#     from aiogram import Bot
#     from bot.utils.config_reader import config
#
#     bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
#     run(bot=bot)
