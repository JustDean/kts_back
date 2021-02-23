from time import time
import json
from vkwave.bots import BaseMiddleware, MiddlewareResult

from app.models import Session


class TurnError(Exception):
    pass


def process_game(storage):
    class Game(BaseMiddleware):
        async def pre_process_event(self, event):
            try:
                ################### process only if the game is on ##########################
                if event['payload'] == '{"command":"game_menu"}' or \
                        event['payload'] == '{"command":"next_round"}' or \
                        event['payload'] == '{"command":"answer"}' or \
                        event['payload'] == '{"command":"time_up"}':
                    performer = event.object.object.message.from_id

                    # showing results do not require authorization
                    if event['results']:
                        return MiddlewareResult(True)

                    ###################### "command":"game_menu" ######################################
                    if event['payload'] == '{"command":"game_menu"}':
                        ####### first entrance
                        if storage[event['conversation_id']]['chooser'] is None:
                            storage[event['conversation_id']]['chooser'] = performer

                            return MiddlewareResult(True)

                        #################### answer was given ############################
                        ####### by caller
                        elif storage[event['conversation_id']]['caller'] == performer:
                            n_round = storage[event['conversation_id']]['round']
                            answer = event['user_text'].replace('[club202343491|bot]', '').lower()
                            correct_answer = storage['quiz'][n_round].answer.lower()

                            ######### correct
                            if answer == correct_answer:
                                ###### last round
                                if n_round == len(storage['quiz']) - 1:
                                    timer = time()
                                    await storage[event['conversation_id']]['timer'].put('timer', timer)

                                    storage[event['conversation_id']]['participants'][performer] += \
                                        event['quiz'][n_round]['points']
                                    storage[event['conversation_id']]['chooser'] = None
                                    storage[event['conversation_id']]['caller'] = None
                                    event['results'] = True
                                    storage[event['conversation_id']]['history'] = \
                                        storage[event['conversation_id']]['participants']

                                    #push to database
                                    session = await Session.query. \
                                        where(Session.conversation_id == event['conversation_id']) \
                                        .gino.first()

                                    await session.update(history=json.dumps(storage[event['conversation_id']['history']]),
                                                         status='finished').apply()

                                    event.object.object.message.payload = '{"command":"menu"}'

                                    return MiddlewareResult(True)
                                else:
                                    timer = time()
                                    await storage[event['conversation_id']]['timer'].put('timer', timer)

                                    storage[event['conversation_id']]['participants'][performer] += \
                                        storage['quiz'][n_round].points
                                    storage[event['conversation_id']]['chooser'] = performer
                                    storage[event['conversation_id']]['caller'] = None  # release caller
                                    storage[event['conversation_id']]['round'] += 1     # next round

                                    if n_round == len(storage['quiz']) - 1:     # upcoming last round
                                        event['last_round'] = True
                                    else:
                                        event['good_call'] = True

                                return MiddlewareResult(True)
                            ############# wrong
                            else:
                                event['wrong'] = True
                                storage[event['conversation_id']]['caller'] = None  # release caller
                                storage[event['conversation_id']]['participants'][performer] -= \
                                    storage['quiz'][n_round].points
                                event.object.object.message.payload = '{"command":"next_round"}'    # get back to the question page

                                return MiddlewareResult(True)
                        ####### not by caller
                        else:
                            raise TurnError
                    ##################### "command":"next_round" #################################
                    elif event['payload'] == '{"command":"next_round"}':

                        ####################### chooser called ############################
                        if performer == storage[event['conversation_id']]['chooser']:
                            return MiddlewareResult(True)

                        ####################### not chooser called ############################
                        else:
                            event['turn_violation'] = True
                            event.object.object.message.payload = '{"command":"game_menu"}'
                            return MiddlewareResult(True)

                    ##################### "command":"answer" #################################
                    elif event['payload'] == '{"command":"answer"}':
                        if storage[event['conversation_id']]['caller'] is None:
                            storage[event['conversation_id']]['caller'] = performer

                            return MiddlewareResult(True)

                        else:
                            raise TurnError
                    ################### "command":"time_up" #########################
                    elif event['payload'] == '{"command":"time_up"}':
                        event.object.object.message.payload = '{"command":"game_menu"}'
                        event['payload'] = '{"command":"game_menu"}'
                        n_round = storage[event['conversation_id']]['round']

                        ####### last round
                        if n_round == len(storage['quiz']) - 1:
                            timer = time()
                            await storage[event['conversation_id']]['timer'].put('timer', timer)

                            storage[event['conversation_id']]['caller'] = None
                            event['results'] = True
                            storage[event['conversation_id']]['history'] = storage[event['conversation_id']][
                                'participants']
                            event.object.object.message.payload = '{"command":"menu"}'

                            return MiddlewareResult(True)

                        else:
                            timer = time()
                            await storage[event['conversation_id']]['timer'].put('timer', timer)

                            storage[event['conversation_id']]['caller'] = None  # release caller
                            storage[event['conversation_id']]['round'] += 1  # next round

                            if n_round == len(storage['quiz']) - 1:  # upcoming last round
                                event['last_round'] = True
                            else:
                                event['good_call'] = True

                        return MiddlewareResult(True)

                ############################# not caller wrote a message ################################
                    else:
                        raise TurnError
                ########################## if not a game - ignore #############################
                else:
                    return MiddlewareResult(True)
            except TurnError:
                return MiddlewareResult(False)

    return Game()
