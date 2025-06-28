from pydantic import BaseModel
from datetime import date
from app.database.entities.enums import Transactiontype
from typing import Optional


class TransactionCreate(BaseModel):
    type: Transactiontype
    value: float
    date: date
    description: Optional[str] = None
