from typing import List

from pydantic import BaseModel


class TodoSchema(BaseModel):
    id: int = 0
    text: str
    completed: bool = False


class TodosSchema(BaseModel):
    objects: List[TodoSchema]
