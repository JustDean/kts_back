from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter,
                         )


help_handler = DefaultRouter()


@simple_bot_message_handler(help_handler, PayloadFilter({"command": "help"}))
async def handler(event):
    return await event.answer(
        message='Я простой бот - квизер. Нажимай "Start", когда будешь готов',
        )
