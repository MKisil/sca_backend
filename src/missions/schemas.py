from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional


class TargetCreate(BaseModel):
    name: str
    country: str
    notes: Optional[str] = ""

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) > 255:
            raise ValueError('Field "name" must be at most 255 characters.')
        return v

    @field_validator('country')
    def validate_country(cls, v):
        if len(v) > 255:
            raise ValueError('Field "country" must be at most 255 characters.')
        return v


class TargetUpdate(BaseModel):
    notes: Optional[str]
    completed: Optional[bool]


class TargetOut(BaseModel):
    id: int
    name: str
    country: str
    notes: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)


class MissionCreate(BaseModel):
    targets: List[TargetCreate]


class AssignCatRequest(BaseModel):
    cat_id: int


class MissionOut(BaseModel):
    id: int
    completed: bool
    cat_id: Optional[int]
    targets: List[TargetOut]

    model_config = ConfigDict(from_attributes=True)
