import asyncio
from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter,
                         )
from bot_v1.keyboards.stage_kb import get_stage_kb


next_stage_handler = DefaultRouter()


# async def main(event):
#     stage_info = event['stage_info']
#     if event['comment']:
#         await event.answer(message=event['comment'])
#
#     return await event.answer(message=stage_info.question,
#                               keyboard=get_stage_kb(stage_info, event['final_stage']).get_keyboard())
#
#
# async def timer(event):
#     await asyncio.sleep(10)
#     return await event.answer(message="too late",
#                               payload='{"command": "next_stage"}')


@simple_bot_message_handler(next_stage_handler, PayloadFilter({"command": "next_stage"}))
async def handler(event):
    # fin, _ = await asyncio.wait([main(event), timer(event)], return_when=asyncio.FIRST_COMPLETED)
    # return fin
    stage_info = event['stage_info']
    if event['comment']:
        await event.answer(message=event['comment'])

    await event.answer(message=stage_info.question,
                       keyboard=get_stage_kb(stage_info, event['final_stage']).get_keyboard())
