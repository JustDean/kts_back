from re import match
import json
from vkwave.bots import BaseMiddleware, MiddlewareResult

from app.models import Session

from bot_v2.consts.payload_consts import (MENU,
                                          HELP,
                                          GAME_MENU,
                                          RESULTS,
                                          PREV_GAME,
                                          END,
                                          TIME)


class RoutingMiddleware(BaseMiddleware):
    def __init__(self):
        from bot_v2.main import storage
        self.storage = storage

    async def pre_process_event(self, event):
        try:
            # first entrance
            if event['user_text'] == "":
                event.object.object.message.payload = MENU
                event['payload'] = MENU

            # help
            elif event['payload'] == HELP:
                event['help'] = True
                event.object.object.message.payload = MENU
                event['payload'] = MENU

            # previous game
            elif event['payload'] == PREV_GAME:
                conversation_id = event['conversation_id']
                prev_game = await Session.query.where(Session.conversation_id == conversation_id).gino.first()

                if prev_game is None:
                    event['error'] = "У вас еще не было игр!"
                else:
                    event['results'] = prev_game

                event.object.object.message.payload = MENU  # redirecting
                event['payload'] = MENU

            # results from game menu
            elif event['payload'] == RESULTS:
                event['results'] = True
                event.object.object.message.payload = GAME_MENU
                event['payload'] = GAME_MENU

            # end
            elif event['payload'] == END:
                conversation_id = event['conversation_id']
                session = await Session.query.where(Session.conversation_id == conversation_id).gino.first()

                score = json.dumps(self.storage[event['conversation_id']]['participants'])
                await session.update(conversation_id=event['conversation_id'],
                                     players_score=score,
                                     status='finished').apply()

                del (self.storage[event['conversation_id']])

                event['results'] = session
                event.object.object.message.payload = MENU
                event['payload'] = MENU

            # reset (development tool)
            elif match(r'!r', event['user_text']):
                event.object.object.message.payload = MENU
                event['payload'] = MENU

            # answer was given
            elif (self.storage[event['conversation_id']]['caller'] is not None) and (event['payload'] != TIME):
                event.object.object.message.payload = GAME_MENU
                event['payload'] = GAME_MENU

        finally:
            return MiddlewareResult(True)
