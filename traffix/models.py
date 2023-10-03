from typing_extensions import Annotated
from typing import Any
from typing import Annotated, Union
from bson import ObjectId
from pydantic import (
    BaseModel,
    PlainSerializer,
    AfterValidator,
    WithJsonSchema,
    Field,
    ConfigDict,
    StringConstraints,
)
from typing import Optional, List
from datetime import datetime
from enum import Enum

from traffix.config import settings


def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]


class RUTypeEnum(str, Enum):
    release = "release"
    update = "update"


class RUBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    estimated_size: Annotated[int, Field(strict=True, le=settings.MAX_RU_SIZE)]
    size: Optional[Annotated[int, Field(strict=True, le=settings.MAX_RU_SIZE)]] = None
    ru_type: RUTypeEnum
    categories: Optional[List[str]] = []
    release_date: datetime
    image_url: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            max_length=settings.MAX_IMAGE_URL_LENGTH,
        ),
    ]
    reviewed: bool = False
    reviewed_date: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RURead(RUBase):
    pass


class RUCreate(RUBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RUUpdate(RUBase):
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class RU(RUBase):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")


class AlertColourEnum(str, Enum):
    primary = "primary"
    secondary = "secondary"
    danger = "danger"
    success = "success"
    warning = "warning"
    info = "info"
    light = "light"
    dark = "dark"


class Alert(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    colour: AlertColourEnum
    title: str
    text: str
