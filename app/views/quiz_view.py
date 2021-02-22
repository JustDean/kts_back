from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import docs, querystring_schema, response_schema

from app.schemas.base_schema import GetListRequest, BaseResponseSchema
from app.schemas.quiz_schema import (GetQuizRequest,
                                     QuizDC,
                                     QuizListDC,
                                     PostQuizRequest
                                     )

from app.responses import json_response


class GetQuizView(web.View):
    @docs(tags=['quiz'])
    @querystring_schema(GetQuizRequest.Schema())
    @response_schema(QuizDC.Schema())
    async def get(self):
        from app.models import Quiz     # due to ImportError
        query = self.request.query

        question_id = int(query.get("id"))

        question = await Quiz.query.where(Quiz.id == question_id).gino.first()

        if question is None:
            raise HTTPNotFound

        return json_response(data=QuizDC.Schema().dump(question.to_dc()))


class ListQuizView(web.View):
    @docs(tags=["quiz"],)
    @querystring_schema(GetListRequest.Schema())
    @response_schema(QuizListDC.Schema(), 200)
    async def get(self):
        from app.models import Quiz
        query = self.request.query

        limit = int(query.get("limit", 100))
        offset = int(query.get("offset", 0))

        questions_all = await Quiz.query.limit(limit).offset(offset).gino.all()

        return json_response(data=QuizListDC.Schema().dump(QuizListDC(questions=[a.to_dc() for a in questions_all])))


class PostQuizView(web.View):
    @docs(tags=['quiz'])
    @querystring_schema(PostQuizRequest.Schema())
    @response_schema(QuizDC.Schema())
    async def post(self):
        from app.models import Quiz     # due to ImportError
        query = self.request.query

        question = query.get("question")
        answer = query.get("answer")
        points = int(query.get("points"))

        quiz = Quiz(question=question,
                    answer=answer,
                    points=points)
        await quiz.create()

        response = await Quiz.query.where(Quiz.question == question).gino.first()

        if response is None:
            raise HTTPNotFound

        return json_response(data=QuizDC.Schema().dump(response.to_dc()))


class DeleteQuizView(web.View):
    @docs(tags=['quiz'])
    @querystring_schema(GetQuizRequest.Schema())
    @response_schema(BaseResponseSchema, 200, description="Question has been deleted")
    async def post(self):
        from app.models import Quiz     # due to ImportError
        query = self.request.query

        question_id = int(query.get('id'))

        await Quiz.delete.where(Quiz.id == question_id).gino.status()

        return json_response(data="The question was deleted")

