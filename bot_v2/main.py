from vkwave.bots import SimpleLongPollBot

from bot_v2.middlewares.routing_middleware import set_routing
from bot_v2.middlewares.session_preprocess import session_check
from bot_v2.middlewares.game_processing import process_game

from bot_v2.routers.help_handler import help_handler
from bot_v2.routers.menu_handler import get_menu
from bot_v2.routers.game_menu import game_menu
from bot_v2.routers.round_handler import next_round
from bot_v2.routers.answer_handler import answer_handler

storage = dict()    # aka cache


async def set_bot(application):
    token = application['config']['vk']['token']
    group_id = application['config']['vk']['group_id']

    bot = SimpleLongPollBot(token, group_id)
#################################################################################################
    bot.middleware_manager.add_middleware(session_check(storage))
    bot.middleware_manager.add_middleware(set_routing(storage))
    bot.middleware_manager.add_middleware(process_game(storage))

    bot.dispatcher.add_router(game_menu(storage))
    bot.dispatcher.add_router(next_round(storage))
    bot.dispatcher.add_router(answer_handler(storage))
    bot.dispatcher.add_router(help_handler)
    # if all else fails
    bot.dispatcher.add_router(get_menu(storage))
###################################################################################################
    bot.run_forever()
