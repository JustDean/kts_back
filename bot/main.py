from vkwave.bots import SimpleLongPollBot


async def set_bot(token, group_id):
    bot = SimpleLongPollBot(token, group_id)

    @bot.message_handler()
    async def handle(event):
        user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.peer_id)).response[0]
        await event.answer(message=f"Привет, {user_data.first_name}.\nЗачем ты отправил мне \"{event.object.object.message.text}\"?")

    bot.run_forever()
