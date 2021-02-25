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


def setup_app():
    app = web.Application()

    set_config(app)
    set_routes(app)
    set_db(app)
    set_bot(app)
    set_jinja(app)
    set_swagger(app)
    set_logging()

    return app


# for testing admin api
def set_testing():
    app = web.Application()

    set_config(app)
    set_routes(app)
    set_db(app)
    # set_bot(app)      # causes an error in ShutDown
    set_jinja(app)
    set_swagger(app)
    set_logging()

    return app


if __name__ == '__main__':
    app = setup_app()
    web.run_app(app, port=app['config']['base']['port'])
