from vkwave.bots import SimpleLongPollBot

from bot_v2.middlewares.routing_middleware import RoutingMiddleware
from bot_v2.middlewares.session_preprocess import SessionMiddleware
from bot_v2.middlewares.game_processing import Game

from bot_v2.routers.menu_handler import menu_handler
from bot_v2.routers.game_menu import game_menu
from bot_v2.routers.round_handler import next_round
from bot_v2.routers.answer_handler import answer_handler

storage = dict()    # aka cache


async def set_bot(application):
    token = application['config']['vk']['token']
    group_id = application['config']['vk']['group_id']

    bot = SimpleLongPollBot(token, group_id)

    bot.middleware_manager.add_middleware(SessionMiddleware())
    bot.middleware_manager.add_middleware(RoutingMiddleware())
    bot.middleware_manager.add_middleware(Game())

    bot.dispatcher.add_router(game_menu(storage))
    bot.dispatcher.add_router(next_round(storage))
    bot.dispatcher.add_router(answer_handler(storage))
    bot.dispatcher.add_router(menu_handler)

    bot.run_forever()
