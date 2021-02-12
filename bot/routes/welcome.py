from vkwave.bots import DefaultRouter, simple_bot_message_handler

from bot.keyboard.welcome_kb import WELCOME_KB

welcome_handler = DefaultRouter()


@simple_bot_message_handler(welcome_handler, )
async def handler(event):
    return await event.answer(
        message="Выберите дальнейшее действие",
        keyboard=WELCOME_KB.get_keyboard(),
    )
