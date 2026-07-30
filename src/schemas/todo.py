from pydantic import BaseModel
from datetime import datetime


class Todo(BaseModel):
    id: int

    title: str
    description: str | None = None
    completed: bool = False
    user_id: int

    created_at: datetime = None
    updated_at: datetime = None
