from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter
                         )

from bot_v2.keyboards.menu_kb import MENU_KB


def get_menu(storage):
    welcome_handler = DefaultRouter()

    @simple_bot_message_handler(welcome_handler, PayloadFilter({"command": "menu"}))
    async def handler(event):
        if event['error']:
            message = f'Произошла ошибка.\n{event["error"]}'

        elif event['results']:
            last_match = storage[event['conversation_id']]['history'][-1]
            res = dict()
            for user in last_match:
                name = await event.api_ctx.users.get(user_ids=user)
                res[name.response[0].last_name] = last_match[user]
            message = f"Финальный счет участников:\n{res}"

        elif event['user_text'] == "":
            message = """Добро пожаловать в свою игру!
                         Выдайте боту права администратора в меню беседы и ознакомтесь с инструкцией."""

        else:
            message = "С возвращением!"

        return await event.answer(message=message,
                                  keyboard=MENU_KB.get_keyboard()
                                  )

    return welcome_handler

