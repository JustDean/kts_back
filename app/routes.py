# from app.views import (index,
#                        GetUserView,
#                        ListUsersView,
#                        GetQuizView,
#                        ListQuizView
#                        )

from app.views import index


def get_routes(application):
    application.router.add_get("/", index)
    # application.router.add_view("/api/users.get", GetUserView)
    # application.router.add_view("/api/users.list", ListUsersView)
    #
    # application.router.add_view("/api/quiz.get", GetQuizView)
    # application.router.add_view("/api/quiz.list", ListQuizView)
