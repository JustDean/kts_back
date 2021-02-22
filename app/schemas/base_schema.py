from marshmallow import Schema, EXCLUDE, fields
from marshmallow_dataclass import dataclass
from dataclasses import field
from typing import List, Optional


class BaseResponseSchema(Schema):
    status = fields.Str()
    data = fields.Dict(allow_none=None)


class BaseDataclassSchema:
    Schema = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class BaseResponse(BaseDataclassSchema):
    status: str
    data = fields.Dict(allow_none=None)


@dataclass
class GetListRequest(BaseDataclassSchema):
    limit: Optional[int] = field(metadata={"required": False}, default=None)
    offset: Optional[int] = field(metadata={"required": False}, default=None)
