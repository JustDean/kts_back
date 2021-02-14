from vkwave.bots import SimpleLongPollBot

from bot.middlewares.user_preprocess import UserMiddleware
from bot.middlewares.session_preprocess import session_check
from bot.middlewares.answer_preprocessor import answer_check

from bot.routes.welcome import welcome_handler
from bot.routes.help import help_handler
from bot.routes.start import start_handler
from bot.routes.next_stage import next_stage_handler
from bot.routes.finita import fin_handle


storage = dict()    # aka cache


async def set_bot(application):
    token = application['config']['vk']['token']
    group_id = application['config']['vk']['group_id']

    bot = SimpleLongPollBot(token, group_id)

    bot.middleware_manager.add_middleware(UserMiddleware())
    bot.middleware_manager.add_middleware(session_check(storage))
    bot.middleware_manager.add_middleware(answer_check(storage))

    bot.dispatcher.add_router(help_handler)
    bot.dispatcher.add_router(start_handler)
    bot.dispatcher.add_router(fin_handle(storage))
    bot.dispatcher.add_router(next_stage_handler)

    # if all else fails
    bot.dispatcher.add_router(welcome_handler)

    bot.run_forever()
