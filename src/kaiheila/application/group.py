from pydantic import BaseModel


class Member(BaseModel):
    id: int


class Group(BaseModel):
    id: str
