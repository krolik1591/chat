from aiohttp import web
from aiohttp.web_request import Request

routes = web.RouteTableDef()


@routes.get('/backend')
async def hello(request: Request):
    return web.Response(text="Hello, world")


@routes.post('/backend/create_fortune_wheel')
async def create_fortune_wheel(request: Request):
    print(await request.post())
    return web.Response(text="OK")


def run(port=8080, loop=None, bot=None):
    app = web.Application()
    app['bot'] = bot
    app.add_routes(routes)
    web.run_app(app, port=port, loop=loop)


if __name__ == "__main__":
    run()

