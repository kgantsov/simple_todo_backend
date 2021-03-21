from typing import Optional
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int = 0
    name: Optional[str]
    email: str
    password: str
