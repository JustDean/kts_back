import operator
import json
from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter
                         )

from bot_v2.keyboards.menu_kb import MENU_KB

from app.models import Session


def get_menu(storage):
    welcome_handler = DefaultRouter()

    @simple_bot_message_handler(welcome_handler, PayloadFilter({"command": "menu"}))
    async def handler(event):
        if event['error']:
            message = f'Произошла ошибка.\n{event["error"]}'

        elif event['results']:
            if event['results'] == 'Special':
                last_match = await Session.query.where(Session.conversation_id == event['conversation_id']).gino.first()
                last_match = json.loads(last_match.players_score)

                res = dict()
                for user in last_match.keys():
                    name = await event.api_ctx.users.get(user_ids=user)
                    res[name.response[0].last_name] = last_match[user]
            else:
                last_match = storage[event['conversation_id']]['history']

                res = dict()
                for user in last_match:
                    name = await event.api_ctx.users.get(user_ids=user)
                    res[name.response[0].last_name] = last_match[user]

            winner = max(res.items(), key=operator.itemgetter(1))[0]
            message = f"Победитель {winner}.\nФинальный счет участников:\n{res}"

        elif event['user_text'] == "":
            message = """Добро пожаловать в свою игру!
                         Выдайте боту права администратора в меню беседы и ознакомтесь с инструкцией."""

        else:
            message = "С возвращением!"

        return await event.answer(message=message,
                                  keyboard=MENU_KB.get_keyboard()
                                  )

    return welcome_handler

