import json

from aiohttp import web
from aiohttp.web_request import Request

routes = web.RouteTableDef()


@routes.get('/info')
async def info(request: Request):
    bot_info = await request.app['bot'].me()
    return web.json_response(text=json.dumps({
        "bot_info": {
            "id": bot_info.id,
            "username": bot_info.username,
            "name": bot_info.full_name,
            "url": f"https://t.me/{bot_info.username}",
        }
    }))
