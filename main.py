import logging
from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
import jinja2
import aiohttp_jinja2

from app.settings import BASE_DIR, get_config
from app.routes import get_routes

from db.db_accessor import db_accessor

from bot_v2.bot_accessor import vk_bot


def set_config(application):
    application['config'] = get_config()


def set_routes(application):
    get_routes(application)


def set_db(application):
    db_accessor.setup(application)


def set_bot(application):
    vk_bot.setup(application)


def set_jinja(application):
    aiohttp_jinja2.setup(application, loader=jinja2.FileSystemLoader(f"{BASE_DIR}/templates"))


def set_swagger(application):
    setup_aiohttp_apispec(
        app=application,
        title="VK-bot documentation",
        version="v1",
        url="/swagger.json",
        swagger_path="/swagger",
    )


def set_logging():
    logging.basicConfig(level=logging.DEBUG)


def setup_app(application):
    set_config(application)
    set_routes(application)
    set_db(application)
    set_bot(application)
    set_jinja(application)
    set_swagger(application)
    set_logging()


app = web.Application()

if __name__ == '__main__':
    setup_app(app)
    web.run_app(app, port=app['config']['base']['port'])
