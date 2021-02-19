from vkwave.bots import BaseMiddleware, MiddlewareResult

from db.models import Quiz


def answer_check(storage):
    class AnswerMiddleware(BaseMiddleware):
        async def pre_process_event(self, event):
            try:
                user = event["current_user"].u_id
                quiz = storage['quiz']
                answer = event.object.object.message.text

                if event.object.object.message.payload == '{"command":"next_stage"}' \
                        or event.object.object.message.payload == '{"command":"finish"}':   # if the game is in progress
                    if quiz[storage[user]['stage'] - 1].correct_answer == answer:
                        event['comment'] = f'Все правильно, это {quiz[storage[user]["stage"] - 1].correct_answer}'
                        storage[user]['score'] += 1
                    else:
                        event['comment'] = f'Увы, но правильный ответ {quiz[storage[user]["stage"] - 1].correct_answer}'
                else:
                    pass

            except AttributeError:
                pass
            finally:
                return MiddlewareResult(True)

        async def post_process_event(self, event):
            try:
                if event.object.object.message.text:
                    event['late'].cancel()
            except AttributeError:
                pass

    return AnswerMiddleware()
