from vkwave.bots import SimpleLongPollBot

from bot.middlewares.user_preprocess import UserMiddleware

from bot.routes.welcome import welcome_handler
from bot.routes.help import help_handler
from bot.routes.start import start_handler


async def set_bot(application):
    token = application['config']['vk']['token']
    group_id = application['config']['vk']['group_id']

    bot = SimpleLongPollBot(token, group_id)

    bot.middleware_manager.add_middleware(UserMiddleware())

    bot.dispatcher.add_router(start_handler)
    bot.dispatcher.add_router(help_handler)
    bot.dispatcher.add_router(welcome_handler)

    bot.run_forever()


# @bot.message_handler()
# async def handle(event):
#     user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.peer_id)).response[0]
#     await event.answer(message=f"Привет, {user_data.first_name}.\nЗачем ты отправил мне \"{event.object.object.message.text}\"?")
