from vkwave.bots import BaseMiddleware, MiddlewareResult

from app.models import Quiz


def session_check(storage):
    class SessionMiddleware(BaseMiddleware):
        async def pre_process_event(self, event):
            try:
                user = event["current_user"].u_id
                event['final_stage'] = False

                if 'quiz' not in storage.keys():  # get quiz into cash.
                    storage['quiz'] = await Quiz.query.gino.all()

                if event.object.object.message.payload == '{"command":"start"}':    # creating new user. when the game is starting
                    storage[user] = {'stage': 0,
                                     'score': 0}

                    stage_n = storage[user]['stage']
                    stage_info = storage['quiz'][stage_n]

                    event["stage_info"] = stage_info

                elif event.object.object.message.payload == '{"command":"next_stage"}':     # user is already playing
                    if storage[user]['stage'] != (len(storage['quiz']) - 2):
                        storage[user]['stage'] += 1
                    else:   # if final stage
                        storage[user]['stage'] += 1
                        event['final_stage'] = True

                    stage_n = storage[user]['stage']
                    stage_info = storage['quiz'][stage_n]

                    event["stage_info"] = stage_info

                else:
                    pass
            except AttributeError:
                pass
            finally:
                return MiddlewareResult(True)

    return SessionMiddleware()
