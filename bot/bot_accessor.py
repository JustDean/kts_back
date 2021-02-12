import asyncio

from bot.main import set_bot


class VKAccessor:
    def __init__(self):
        self.token = None
        self.group_id = None

    def setup(self, application):
        application.on_startup.append(self._on_connect)
        application.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, application):
        self.token = application['config']['vk']['token']
        self.group_id = application['config']['vk']['group_id']

        application['bot'] = asyncio.create_task(set_bot(application))

    @staticmethod
    async def _on_disconnect(application):
        application['bot'].cancel()
        await application['bot']


vk_bot = VKAccessor()
