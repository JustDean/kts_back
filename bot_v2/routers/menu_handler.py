import operator
from json import loads
from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter
                         )

from bot_v2.keyboards.menu_kb import MENU_KB

menu_handler = DefaultRouter()


@simple_bot_message_handler(menu_handler, PayloadFilter({"command": "menu"}))
async def handler(event):
    if event['error']:
        message = f'Произошла ошибка.\n{event["error"]}'

    elif event['results']:
        last_match = loads(event['results'].players_score)

        res = dict()
        for user in last_match.keys():
            name = await event.api_ctx.users.get(user_ids=user)
            res[name.response[0].last_name] = last_match[user]

        winner = max(res.items(), key=operator.itemgetter(1))[0]
        message = f"Победитель {winner}.\nФинальный счет участников:\n{res}"

    elif event['help']:
        message = """
        Это своя игра.
        Я буду задавать вопросы по теме "география", а ты попытайся отвечать на них.
        На ответ дается одна минут (1 мин.).
        Если знаешь ответ, нажимай кнопку \"Ответить\" и пиши ответ.
        Ответ должен быть написан правильно, иначе он не защитается. Регистр (большие или маленькие буквы) не важен.
        Пожалуй, все. Удачи!
        """

    elif event['user_text'] == "":
        message = """Добро пожаловать в свою игру!
                     Выдайте боту права администратора в меню беседы и ознакомтесь с инструкцией."""

    else:
        message = "С возвращением!"

    return await event.answer(message=message,
                              keyboard=MENU_KB.get_keyboard()
                              )
