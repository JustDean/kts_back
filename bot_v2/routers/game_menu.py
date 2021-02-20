from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter,
                         )
from bot_v2.keyboards.game_menu_kb import GAME_MENU_KB


def game_menu(storage):
    game_menu = DefaultRouter()

    @simple_bot_message_handler(game_menu, PayloadFilter({"command": "game_menu"}))
    async def handler(event):
        chooser = await event.api_ctx.users.get(user_ids=storage[event['conversation_id']]['chooser'])
        chooser = chooser.response[0].last_name

        if event['turn_violation']:
            pretender = await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)
            pretender = pretender.response[0].last_name

            return await event.answer(
                message=f"{pretender}, Вы не можете начать игру.\n{chooser} может.",
                keyboard=GAME_MENU_KB.get_keyboard()
            )

        elif event['results']:
            participants = storage[event['conversation_id']]['participants']
            res = dict()
            for user in participants:
                name = await event.api_ctx.users.get(user_ids=user)
                res[name.response[0].last_name] = participants[user]
            message = f"Счет участников:\n{res}"

            return await event.answer(
                message=message,
                keyboard=GAME_MENU_KB.get_keyboard()
            )

        elif event['good_call']:

            return await event.answer(
                message=f"Хорошо, идем дальше!\nРаунд: {storage[event['conversation_id']]['round'] + 1}.\nНачинай, {chooser}",
                keyboard=GAME_MENU_KB.get_keyboard()
            )

        elif event['last_round']:

            return await event.answer(
                message=f"Правильный ответ!\nПоследний раунд.\nНачинай, {chooser}",
                keyboard=GAME_MENU_KB.get_keyboard()
            )

        else:
            return await event.answer(
                message=f"Раунд: {storage[event['conversation_id']]['round'] + 1}.\nНачинай, {chooser}",
                keyboard=GAME_MENU_KB.get_keyboard()
                )

    return game_menu
