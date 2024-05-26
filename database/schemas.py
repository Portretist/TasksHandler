from typing import List, Optional

from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True


class CreateTagSchema(BaseSchema):
    name: str


class GetTagSchema(CreateTagSchema):
    id: int


class CreateTaskSchema(BaseSchema):
    heading: str
    description: str

    deadline: Optional[str] = None
    tags: Optional[List[str]] = []


class EditTaskSchema(CreateTaskSchema):
    heading: Optional[str] = None
    description: Optional[str] = None
