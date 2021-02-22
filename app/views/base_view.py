from aiohttp import web


def index(_):
    return web.Response(text="Hello, world")