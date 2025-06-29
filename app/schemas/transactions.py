from pydantic import BaseModel
from datetime import date, datetime
from app.database.entities.enums import TransactionType
from typing import Optional


class TransactionCreate(BaseModel):
    type: TransactionType
    value: float
    date: date
    description: Optional[str] = None


class TransactionRead(BaseModel):
    id: int
    user_id: int
    type: TransactionType
    value: float
    date: date
    description: Optional[str] = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class TransactionUpdate(BaseModel):
    type: Optional[TransactionType] = None
    value: Optional[float] = None
    transaction_date: Optional[date] = None
    description: Optional[str] = None



class SummaryRead(BaseModel):
    total_income: float
    total_expense: float
    balance: float
