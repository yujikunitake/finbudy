from pydantic import BaseModel
from datetime import date
from app.database.entities.enums import Transactiontype
from typing import Optional


class TransactionCreate(BaseModel):
    user_id: int
    type: Transactiontype
    value: float
    date: date
    description: Optional[str] = None
