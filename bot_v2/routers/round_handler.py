import asyncio
from time import time
from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter,
                         )
from vkwave.bots.storage.types import Key

from bot_v2.keyboards.round_kb import ROUND_KB
from bot_v2.keyboards.time_up import TIME


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
            my_key = Key("timer")
            timer = time()
            await storage[event['conversation_id']]['timer'].put(my_key, timer)

            await event.answer(
                message=f"{question}",
                keyboard=ROUND_KB.get_keyboard()
                )

            await asyncio.sleep(10)
            get_timer = await storage[event['conversation_id']]['timer'].get("timer")
            if get_timer == timer:
                return await event.answer(message='Время вышло!',
                                          keyboard=TIME.get_keyboard())
            else:
                return None

    return help_handler
