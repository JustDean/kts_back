from vkwave.bots import (DefaultRouter,
                         simple_bot_message_handler,
                         PayloadFilter,
                         )


def answer_handler(storage):
    answer_handler = DefaultRouter()

    @simple_bot_message_handler(answer_handler, PayloadFilter({"command": "answer"}))
    async def handler(event):
        caller = await event.api_ctx.users.get(user_ids=storage[event['conversation_id']]['caller'])
        caller = caller.response[0].last_name

        return await event.answer(message=f'Отвечает участник {caller}')

    return answer_handler
