from db.db_accessor import db
from sqlalchemy.dialects.postgresql import JSONB


class DCConverter:
    def to_dc(self):
        raise NotImplementedError


class Quiz(db.Model, DCConverter):
    __tablename__ = "quiz"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, unique=True)
    answer = db.Column(db.String)
    points = db.Column(db.Integer)

    def to_dc(self):
        from app.schemas.quiz_schema import QuizDC
        return QuizDC.Schema().load(self.__values__)


class Session(db.Model, DCConverter):
    __tablename__ = "sessions"

    conversation_id = db.Column(db.Integer, primary_key=True)
    players_score = db.Column(JSONB, nullable=False, server_default="{}")
    status = db.Column(db.String)

    def to_dc(self):
        from app.schemas.sessions_schema import SessionDC
        return SessionDC.Schema().load(self.__values__)
