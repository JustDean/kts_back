from time import time
from json import dumps
from vkwave.bots import BaseMiddleware, MiddlewareResult

from app.models import Session

from bot_v2.consts.payload_consts import (GAME_MENU,
                                          MENU,
                                          ROUND,
                                          ANSWER,
                                          TIME,
                                          )


class TurnError(Exception):
    pass


class Game(BaseMiddleware):
    def __init__(self):
        from bot_v2.main import storage
        self.storage = storage

    async def pre_process_event(self, event):
        try:
            # process only if the game is on
            if event['payload'] == GAME_MENU or \
                    event['payload'] == ROUND or \
                    event['payload'] == ANSWER or \
                    event['payload'] == TIME:

                performer = event.object.object.message.from_id
                
                # showing results do not require authorization. So we pass it through
                if event['results']:
                    return MiddlewareResult(True)

                # GAME_MENU command
                if event['payload'] == GAME_MENU:
                    # game starting
                    if self.storage[event['conversation_id']]['chooser'] is None:
                        self.storage[event['conversation_id']]['chooser'] = performer

                        return MiddlewareResult(True)

                    # an answer was given
                    # by caller
                    elif self.storage[event['conversation_id']]['caller'] == performer:
                        n_round = self.storage[event['conversation_id']]['round']
                        answer = event['user_text'].lower()
                        correct_answer = self.storage[event['conversation_id']]['quiz'][n_round].answer.lower()
                        performer = event.object.object.message.from_id

                        # correct answer
                        if answer == correct_answer:
                            # final round
                            if n_round == len(self.storage[event['conversation_id']]['quiz']) - 1:
                                timer = time()
                                await self.storage[event['conversation_id']]['timer'].put('timer', timer)

                                self.storage[event['conversation_id']]['participants'][performer] += \
                                    self.storage[event['conversation_id']]['quiz'][n_round].points  # player scored
                                self.storage[event['conversation_id']]['chooser'] = None  # release all
                                self.storage[event['conversation_id']]['caller'] = None

                                res = dumps(self.storage[event['conversation_id']]['participants'])  # get result

                                # push to database
                                session = await Session.query. \
                                    where(Session.conversation_id == event['conversation_id']) \
                                    .gino.first()

                                await session.update(players_score=res,
                                                     status='finished').apply()

                                del (self.storage[event['conversation_id']])    # delete from cash

                                conversation_id = event['conversation_id']
                                event['results'] = await Session.query. \
                                    where(Session.conversation_id == conversation_id).gino.first()
                                event.object.object.message.payload = MENU  # redirecting
                                event['payload'] = MENU

                            # any other rounds
                            else:
                                timer = time()
                                await self.storage[event['conversation_id']]['timer'].put('timer',
                                                                                          timer)  # release timer

                                self.storage[event['conversation_id']]['participants'][performer] += \
                                    self.storage[event['conversation_id']]['quiz'][n_round].points
                                self.storage[event['conversation_id']]['chooser'] = performer
                                self.storage[event['conversation_id']]['caller'] = None  # release caller
                                self.storage[event['conversation_id']]['round'] += 1  # next round

                                if n_round == len(
                                        self.storage[event['conversation_id']]['quiz']) - 1:  # upcoming last round
                                    event['last_round'] = True
                                else:
                                    event['good_call'] = True

                            return MiddlewareResult(True)
                        # wrong answer
                        else:
                            event['wrong'] = True
                            self.storage[event['conversation_id']]['caller'] = None  # release caller
                            self.storage[event['conversation_id']]['participants'][performer] -= \
                                self.storage[event['conversation_id']]['quiz'][n_round].points  # reduce points
                            event.object.object.message.payload = ROUND    # get back to the question page
                            event['payload'] = ROUND

                            return MiddlewareResult(True)
                    # not by caller (out of turn)
                    else:
                        raise TurnError
                # next round
                elif event['payload'] == ROUND:

                    # chooser called
                    if performer == self.storage[event['conversation_id']]['chooser']:
                        return MiddlewareResult(True)

                    # not a chooser called
                    else:
                        event['turn_violation'] = True
                        event.object.object.message.payload = MENU
                        event['payload'] = MENU

                        return MiddlewareResult(True)

                # answer
                elif event['payload'] == ANSWER:
                    # set caller if there is no one
                    if self.storage[event['conversation_id']]['caller'] is None:
                        self.storage[event['conversation_id']]['caller'] = performer

                        return MiddlewareResult(True)

                    else:
                        raise TurnError
                # time up
                elif event['payload'] == TIME:
                    n_round = self.storage[event['conversation_id']]['round']   # round stays the same

                    # final round
                    if n_round == len(self.storage[event['conversation_id']]['quiz']) - 1:
                        timer = time()
                        await self.storage[event['conversation_id']]['timer'].put('timer', timer)

                        self.storage[event['conversation_id']]['chooser'] = None  # release all
                        self.storage[event['conversation_id']]['caller'] = None

                        res = dumps(self.storage[event['conversation_id']]['participants'])  # get result

                        # push to database
                        session = await Session.query. \
                            where(Session.conversation_id == event['conversation_id']) \
                            .gino.first()

                        await session.update(players_score=res,
                                             status='finished').apply()

                        del (self.storage[event['conversation_id']])  # delete from cash

                        conversation_id = event['conversation_id']
                        event['results'] = await Session.query.\
                            where(Session.conversation_id == conversation_id).gino.first()
                        event.object.object.message.payload = MENU  # redirecting
                        event['payload'] = MENU

                    # any other rounds
                    else:
                        timer = time()
                        await self.storage[event['conversation_id']]['timer'].put('timer', timer)  # release timer

                        self.storage[event['conversation_id']]['caller'] = None
                        self.storage[event['conversation_id']]['round'] += 1

                        if n_round == len(
                                self.storage[event['conversation_id']]['quiz']) - 1:  # upcoming last round
                            event['last_round'] = True

                        event.object.object.message.payload = GAME_MENU
                        event['payload'] = GAME_MENU  # redirecting

                    return MiddlewareResult(True)

            # not a caller wrote a message
                else:
                    raise TurnError
            # if not part of a game - just ignore
            else:
                return MiddlewareResult(True)

        except TurnError:
            return MiddlewareResult(False)
