from re import match
from vkwave.bots import BaseMiddleware, MiddlewareResult


def set_routing(storage):
    class RoutingMiddleware(BaseMiddleware):
        async def pre_process_event(self, event):
            try:
                ################# SET ROUTES FOR MENU #######################
                if (event['user_text'] == "") or \
                        (event['user_text'] == f"[club{event['group_id']}|@club{event['group_id']}] Понял!"):
                    event.object.object.message.payload = '{"command":"menu"}'
                    event['payload'] = '{"command":"menu"}'

                ######################### results from main menu ############################
                elif event['user_text'] == f"[club{event['group_id']}|@club{event['group_id']}] Прошлая игра!":
                    if event['conversation_id'] not in storage.keys():
                        event['error'] = "У вас еще не было игр!"
                    else:
                        event['results'] = True

                ######################### results from game menu ############################
                elif event['user_text'] == f"[club{event['group_id']}|@club{event['group_id']}] Результаты!":
                    event['results'] = True

                ######################### end game ############################
                elif event['user_text'] == f"[club{event['group_id']}|@club{event['group_id']}] Закончить!":
                    storage[event['conversation_id']]['history'].append(storage[event['conversation_id']]['participants'])  # adding game results in a history
                    storage[event['conversation_id']]['round'] = 0
                    storage[event['conversation_id']]['caller'] = None
                    storage[event['conversation_id']]['chooser'] = None

                    event['results'] = True

                ######################### answer was given ############################
                elif match('\[club202343491\|bot]', event['user_text']):
                    event.object.object.message.payload = '{"command":"game_menu"}'
                    event['payload'] = '{"command":"game_menu"}'

                elif match(r'!r', event['user_text']):
                    event.object.object.message.payload = '{"command":"menu"}'
                    event['payload'] = '{"command":"menu"}'

            except:
                pass
            finally:
                return MiddlewareResult(True)

    return RoutingMiddleware()
