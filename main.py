import logging
from aiohttp import web

from settings.settings import get_config
from db.db_accessor import db_accessor
from bot.bot_accessor import vk_bot


def set_config(application):
    application['config'] = get_config()


def set_db(application):
    db_accessor.setup(application)


def set_bot(application):
    vk_bot.setup(application)


def set_logging():
    logging.basicConfig(level=logging.DEBUG)


def setup_app(application):
    set_config(application)
    set_db(application)
    set_bot(application)
    set_logging()


app = web.Application()

if __name__ == '__main__':
    setup_app(app)
    web.run_app(app, port=app['config']['base']['port'])
