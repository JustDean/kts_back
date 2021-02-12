from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter,
                         )


start_handler = DefaultRouter()


@simple_bot_message_handler(start_handler, PayloadFilter({"command": "start"}))
async def handler(event):
    return await event.answer(
        message="Не могу. Контент еще не подъехал",
    )
