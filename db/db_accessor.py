from gino import Gino
from aiohttp import web


db = Gino()


class PsqlAccessor:
    def __init__(self):
        from db.models import User, Quiz

        self.user = User
        self.quiz = Quiz
        self.db = None

    def setup(self, application):
        application.on_startup.append(self._on_connect)
        application.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, application: web.Application):
        self.config = application["config"]["postgres"]
        await db.set_bind(self.config["db_url"])
        self.db = db
        application["db"] = self

    async def _on_disconnect(self, _):
        if self.db is not None:
            await self.db.pop_bind().close()


db_accessor = PsqlAccessor()
