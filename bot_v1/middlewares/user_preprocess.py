from vkwave.bots import BaseMiddleware, MiddlewareResult

from app.models import User


class UserMiddleware(BaseMiddleware):
    async def pre_process_event(self, event):
        try:
            user_id = event.object.object.message.from_id

            user = await User.query.where(User.u_id == user_id).gino.first()

            if user is None:
                user_data = (await event.api_ctx.users.get(user_ids=user_id)).response[0]
                user = await User.create(u_id=user_id,
                                         first_name=user_data.first_name,
                                         last_name=user_data.last_name,
                                         )

            event["current_user"] = user

        except AttributeError:
            pass
        finally:
            return MiddlewareResult(True)
