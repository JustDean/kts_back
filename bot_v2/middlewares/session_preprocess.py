from json import dumps
from vkwave.bots import BaseMiddleware, MiddlewareResult
from vkwave.bots.storage.storages import Storage

from app.models import Quiz, Session

from bot_v2.consts.payload_consts import MENU, GAME_MENU


# noinspection PyArgumentList
class SessionMiddleware(BaseMiddleware):
    def __init__(self):
        from bot_v2.main import storage
        self.storage = storage

    async def pre_process_event(self, event):
        try:
            # creating aliases and special variables
            # basis
            event['error'] = False
            event['results'] = False
            event['help'] = False
            event['turn_violation'] = False
            event['wrong'] = False
            event['good_call'] = False
            event['last_round'] = False
            event['time_up'] = False
            # creating shortcuts
            event['user_text'] = event.object.object.message.text
            event['conversation_id'] = event.object.object.message.peer_id
            event['group_id'] = event.object.group_id
            event['payload'] = event.object.object.message.payload

            # creating new session in cache. And adding to the db (altering in case game was played before)
            if event['payload'] == GAME_MENU and \
                    event['conversation_id'] not in self.storage.keys():
                fetch_users = \
                    await event.api_ctx.messages.get_conversation_members(peer_id=event['conversation_id'],
                                                                          group_id=event['group_id'])

                fetch_quiz = await Quiz.query.gino.all()

                self.storage[event['conversation_id']] = {"participants": dict(),
                                                          "round": 0,
                                                          "quiz": fetch_quiz,
                                                          "caller": None,
                                                          "chooser": None,
                                                          "timer": Storage()}

                users = [user for user in fetch_users.response.profiles]
                for user in range(len(users)):
                    self.storage[event['conversation_id']]["participants"][users[user].id] = 0   # set score to 0

                # adding to db
                players_json = dumps(self.storage[event['conversation_id']]['participants'], sort_keys=True)

                conversation_id = event['conversation_id']
                current_session = await Session.query.where(Session.conversation_id == conversation_id).gino.first()
                # never played before (altering)
                if current_session is None:
                    session = Session(conversation_id=event['conversation_id'],
                                      players_score=players_json,
                                      status='running')

                    await session.create()
                # have played before (creating new)
                else:
                    await current_session.update(conversation_id=event['conversation_id'],
                                                 players_score=players_json,
                                                 status='running').apply()

        except:
            # In case bot wasn't set as the admin
            if event['payload'] != MENU:
                event['error'] = "Дайте боту права администратора в меню беседы. И попробуйте снова."
                event.object.object.message.payload = MENU
                event['payload'] = MENU
        finally:
            return MiddlewareResult(True)
