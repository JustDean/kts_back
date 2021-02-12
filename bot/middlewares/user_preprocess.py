from vkwave.bots import BaseMiddleware, MiddlewareResult

from db.models import User


class UserMiddleware(BaseMiddleware):
    async def pre_process_event(self, event):
        user_id = event.object.object.message.from_id

        user = await User.query.where(User.u_id == user_id).gino.all()

        if user is None:
            user_data = await event.api_ctx.users.get(user_ids=user_id)
            user = await User.create(u_id=user_id,
                                     first_name=user_data.response[0].first_name,
                                     last_name=user_data.response[0].last_name,
                                     )

        event["current_user"] = user
        return MiddlewareResult(True)
