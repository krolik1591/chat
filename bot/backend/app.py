import json

from aiohttp import web
from aiohttp.web_request import Request
import aiohttp_cors

routes = web.RouteTableDef()


@routes.get('/backend')
async def hello(request: Request):
    return web.Response(text="Hello, world")


@routes.get('/backend/get_fortune_wheel')
async def is_exist_wheel(request: Request):
    hui = {
        'ticket_cost': 10,
        'date_creature': '2021-10-10',
        'date_end': '2021-10-11',
    }
    # return web.Response(text=json.dumps(hui))
    return web.json_response(text='false')


@routes.post('/backend/create_fortune_wheel')
async def create_fortune_wheel(request: Request):
    form_data = await request.json()
    # form_data.ticket_cost  # is number
    # form_data.date_end  # is future date
    print(form_data)
    # todo validate and put to db
    return web.Response(text='{"ok": "ok"}')


def run(port=8080, loop=None, bot=None):
    app = web.Application()
    app['bot'] = bot
    app.add_routes(routes)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*")
    })
    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(app, port=port, loop=loop)


if __name__ == "__main__":
    run()
