from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter,
                         )

help_handler = DefaultRouter()


@simple_bot_message_handler(help_handler, PayloadFilter({"command": "help"}))
async def handler(event):
    return await event.answer(
        message=
        """
        Я простой бот - квизер.\n
        Я буду задавать тебе вопросы а ты выбирай правильный ответ из списка.
        Используй кнопки для ответа на вопросы. Все просто правда?\n
        Нажимай \"начать\", когда будешь готов.
        """,
        )
