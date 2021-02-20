from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter,
                         )

from bot_v2.keyboards.help_kb import AGREED_KB


help_handler = DefaultRouter()


@simple_bot_message_handler(help_handler, PayloadFilter({"command": "help"}))
async def handler(event):
    return await event.answer(
        message=
        """
        Это своя игра.
        
        """,
        keyboard=AGREED_KB.get_keyboard()
        )
