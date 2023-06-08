import json
import time

from aiohttp import web
from aiohttp.web_request import Request
import aiohttp_cors

from bot.db.methods import add_wheel_of_fortune_settings

routes = web.RouteTableDef()


@routes.get('/')
async def hello(request: Request):
    return web.Response(text="Hello, world")


@routes.get('/get_fortune_wheel')
async def is_exist_wheel(request: Request):
    hui = {
        'ticket_cost': 10,
        'date_creature': '2021-10-10',
        'date_end': '2021-10-11',
    }
    # return web.Response(text=json.dumps(hui))
    return web.json_response(text='false')


@routes.post('/create_fortune_wheel')
async def create_fortune_wheel(request: Request):
    form_data = await request.json()
    ticket_cost = form_data['ticket_cost']
    try:
        ticket_cost = int(ticket_cost)
    except ValueError:
        return web.Response(text='"Ticket cost must be a number"', status=400)

    date_end = form_data['end_date']
    if date_end < time.time():
        return web.Response(text='"Date end must be in the future"')

    winner_list = json.dumps(form_data['distribution'])
    await add_wheel_of_fortune_settings(form_data['ticket_cost'], form_data['commission'], winner_list, form_data['end_date'])
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
