from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter,
                         )
from bot_v1.keyboards.welcome_kb import WELCOME_KB


def fin_handle(storage):
    finita_handler = DefaultRouter()

    @simple_bot_message_handler(finita_handler, PayloadFilter({"command": "finish"}))
    async def handler(event):
        return await event.answer(
            message=f"""Вот и все, {event['current_user'].first_name}
            Ты набрал(а) {storage[event['current_user'].u_id]['score']} из {len(storage['quiz'])} баллов""",
            keyboard=WELCOME_KB.get_keyboard(),
        )

    return finita_handler
