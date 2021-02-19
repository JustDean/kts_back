from asyncio import sleep

from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter,
                         )
from bot_v1.keyboards.stage_kb import get_stage_kb


start_handler = DefaultRouter()


@simple_bot_message_handler(start_handler, PayloadFilter({"command": "start"}))
async def handler(event):
    await event.answer(message=f"Отлично! Поехали, {event['current_user'].first_name}!")
    await sleep(.5)  # give a second to think
    stage_info = event['stage_info']

    return await event.answer(
        message=stage_info.question,
        keyboard=get_stage_kb(stage_info, False).get_keyboard(),
    )
