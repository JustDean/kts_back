from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter,
                         )
from bot_v2.keyboards.round_kb import ROUND_KB


def next_round(storage):
    help_handler = DefaultRouter()

    @simple_bot_message_handler(help_handler, PayloadFilter({"command": "next_round"}))
    async def handler(event):
        n_round = storage[event['conversation_id']]['round']
        question = storage['quiz'][n_round].question

        if event['wrong']:
            return await event.answer(
                message=f"Неверный ответ. \nПовторю вопрос: {question}",
                keyboard=ROUND_KB.get_keyboard()
            )
        else:
            return await event.answer(
                message=f"{question}",
                keyboard=ROUND_KB.get_keyboard()
                )

    return help_handler
