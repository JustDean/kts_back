from vkwave.bots import BaseMiddleware, MiddlewareResult

from db.models import Quiz


def session_check(storage):
    class SessionMiddleware(BaseMiddleware):
        async def pre_process_event(self, event):
            try:
                ################# CREATING SPECIAL VARIABLES #######################
                event['error'] = False
                event['results'] = False
                event['turn_violation'] = False
                event['wrong'] = False
                event['good_call'] = False
                event['last_round'] = False


                # creating shortcuts
                event['user_text'] = event.object.object.message.text
                event['conversation_id'] = event.object.object.message.peer_id
                event['group_id'] = event.object.group_id
                event['payload'] = event.object.object.message.payload

                #################### get questions into the cache ######################
                if 'quiz' not in storage.keys():
                    storage['quiz'] = await Quiz.query.gino.all()

                #################### creating new session in cache ######################
                if event['payload'] == '{"command":"game_menu"}' and \
                        event['conversation_id'] not in storage.keys():
                    fetch_users = \
                        await event.api_ctx.messages.get_conversation_members(peer_id=event['conversation_id'],
                                                                              group_id=event['group_id'])

                    storage[event['conversation_id']] = {"participants": dict(),
                                                         "round": 0,
                                                         "caller": None,
                                                         "chooser": None,
                                                         "history": []}
                    current_store = storage[event['conversation_id']]

                    users = [user for user in fetch_users.response.profiles]
                    for user in range(len(users)):
                        current_store["participants"][users[user].id] = 0

                ##########################################################################
            except:
                #################### In case bot wasn't set as the admin ######################
                if event['payload'] != '{"command":"menu"}':
                    event['error'] = "Дайте боту права администратора в меню беседы. И попробуйте снова."
                    event.object.object.message.payload = '{"command":"menu"}'
            finally:
                return MiddlewareResult(True)

    return SessionMiddleware()
