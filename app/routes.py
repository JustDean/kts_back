from app.views.base_view import index
from app.views.quiz_view import (GetQuizView,
                                 ListQuizView,
                                 PostQuizView,
                                 DeleteQuizView
                                 )
from app.views.session_view import GetSessionView, ListSessionView, DeleteSessionView


def get_routes(application):
    application.router.add_get("/", index)
    application.router.add_view("/api/quiz.get", GetQuizView)
    application.router.add_view("/api/quiz.list", ListQuizView)
    application.router.add_view("/api/quiz.post", PostQuizView)
    application.router.add_view("/api/quiz.delete", DeleteQuizView)

    application.router.add_view("/api/session.get", GetSessionView)
    application.router.add_view("/api/session.list", ListSessionView)
    application.router.add_view("/api/session.delete", DeleteSessionView)

