from typing import List
from marshmallow_dataclass import dataclass
from dataclasses import field

from app.schemas.base_schema import BaseDataclassSchema


@dataclass
class GetQuizRequest(BaseDataclassSchema):
    id: int


@dataclass
class PostQuizRequest(BaseDataclassSchema):
    question: str
    answer: str
    points: int


@dataclass
class QuizDC(BaseDataclassSchema):
    id: int
    question: str
    answer: str
    points: int


@dataclass
class QuizListDC(BaseDataclassSchema):
    questions: List[QuizDC] = field(metadata={"required": True}, default_factory=list)
