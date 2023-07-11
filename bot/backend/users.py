from aiohttp import web
from aiohttp.web_request import Request

routes = web.RouteTableDef()


@routes.post('/users/ban')
async def ban_user(request: Request):
    form_data = await request.json()
    print(form_data)
    return web.Response(text='{"ok": "ok"}')
