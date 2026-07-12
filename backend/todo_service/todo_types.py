from typing import TypedDict, Literal
from datetime import datetime

class TodoItem(TypedDict):
    title: str
    priority: Literal["high", "medium", "low"]
    created_at: datetime
    completed: bool = False

