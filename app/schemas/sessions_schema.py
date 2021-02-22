from typing import List, Any
from marshmallow_dataclass import dataclass
from dataclasses import field

from app.schemas.base_schema import BaseDataclassSchema


@dataclass
class GetSessionRequest(BaseDataclassSchema):
    conversation_id: int


@dataclass
class SessionDC(BaseDataclassSchema):
    conversation_id: int
    players_score: Any
    status: str


@dataclass
class SessionListDC(BaseDataclassSchema):
    sessions: List[SessionDC] = field(metadata={"required": True}, default_factory=list)
