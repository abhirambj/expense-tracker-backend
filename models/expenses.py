from pydantic import BaseModel
from typing import Optional


class Expense(BaseModel):
    id: int
    name: str
    amount: float
    date: str
    category: Optional[str] = None
    description: Optional[str] = None
