from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter,
                         )

from bot_v2.keyboards.help_kb import AGREED_KB


help_handler = DefaultRouter()


@simple_bot_message_handler(help_handler, PayloadFilter({"command": "help"}))
async def handler(event):
    return await event.answer(
        message=
        """
        Это своя игра.
        Я буду задавать вопросы по теме "география", а ты попытайся отвечать на них.
        На ответ дается одна минут (1 мин. 00 сек.).
        Если знаешь ответ, нажимай кнопку \"Ответить\" и пиши ответ.
        При ответе надо обращаться к боту в следующем формате напиши символ @, выбери из списка бота и пиши свой ответ.
        Ответ должен быть написан правильно, иначе он не защитается. Регистр (большие или маленькие буквы) не важен.
        Пожалуй, все. Удачи!
        """,
        keyboard=AGREED_KB.get_keyboard()
        )
