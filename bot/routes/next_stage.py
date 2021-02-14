from asyncio import sleep
from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter,
                         )
from bot.keyboards.stage_kb import get_stage_kb


next_stage_handler = DefaultRouter()


@simple_bot_message_handler(next_stage_handler, PayloadFilter({"command": "next_stage"}))
async def handler(event):
    stage_info = event['stage_info']

    if event['comment']:
        await event.answer(message=event['comment'])
        await sleep(.3)

    return await event.answer(
        message=stage_info.question,
        keyboard=get_stage_kb(stage_info, event['final_stage']).get_keyboard(),
    )
