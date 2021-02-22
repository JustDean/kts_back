from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import docs, querystring_schema, response_schema

from app.schemas.base_schema import GetListRequest, BaseResponseSchema
from app.schemas.sessions_schema import GetSessionRequest, SessionDC, SessionListDC

from app.responses import json_response


class GetSessionView(web.View):
    @docs(tags=['session'])
    @querystring_schema(GetSessionRequest.Schema())
    @response_schema(SessionDC.Schema())
    async def get(self):
        from app.models import Session     # due to ImportError
        query = self.request.query

        conversation_id = int(query.get("conversation_id"))

        response = await Session.query.where(Session.conversation_id == conversation_id).gino.first()

        if response is None:
            raise HTTPNotFound

        return json_response(data=SessionDC.Schema().dump(response.to_dc()))


class ListSessionView(web.View):
    @docs(tags=["session"],)
    @querystring_schema(GetListRequest.Schema())
    @response_schema(SessionListDC.Schema(), 200)
    async def get(self):
        from app.models import Session
        query = self.request.query

        limit = int(query.get("limit", 100))
        offset = int(query.get("offset", 0))

        all_sessions = await Session.query.limit(limit).offset(offset).gino.all()

        return json_response(data=SessionListDC.Schema()
                             .dump(SessionListDC(sessions=[a.to_dc() for a in all_sessions])))


class DeleteSessionView(web.View):
    @docs(tags=['session'])
    @querystring_schema(GetSessionRequest.Schema())
    @response_schema(BaseResponseSchema, 200, description="Session has been deleted")
    async def post(self):
        from app.models import Session     # due to ImportError
        query = self.request.query

        conversation_id = int(query.get('conversation_id'))

        check = await Session.query.where(Session.conversation_id == conversation_id).gino.first()

        if check is None:
            return json_response(data="No question with this id was found")

        else:
            await Session.delete.where(Session.conversation_id == conversation_id).gino.status()

        return json_response(data="The question was deleted")
