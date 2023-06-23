import hashlib
import hmac
import json
from urllib.parse import unquote

import aiohttp_cors
from aiohttp import web
from aiohttp.web import middleware
from aiohttp.web_request import Request

from bot.backend.wof import routes as wof_routers


@middleware
async def check_auth_middleware(request: Request, handler):
    bot_token = request.app['bot'].token
    if request.method != "OPTIONS":
        is_valid, tg_id = check_auth(request.headers.get("X-Auth"), bot_token)
        if not is_valid or tg_id not in (185520398,):  # todo check admin list
            return web.Response(text="Unauthorized", status=401)

    return await handler(request)


# todo as middleware
def check_auth(auth: str, bot_token: str):
    if not auth:
        return None, None

    bot_token = hashlib.sha256(bot_token.encode()).digest()

    auth = json.loads(unquote(auth))
    token = "\n".join(sorted([f"{k}={v}" for k, v in auth.items() if k != "hash"]))
    token_hash = hmac.new(bot_token, token.encode(), hashlib.sha256).hexdigest()

    return auth["hash"] == token_hash, auth["id"]


def run(port=8080, loop=None, bot=None, ssl_context=None):
    app = web.Application(middlewares=[check_auth_middleware])
    app['bot'] = bot
    app.add_routes(wof_routers)

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
    run(bot=bot)
