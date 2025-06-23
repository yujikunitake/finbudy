from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str
    birth_date: date


class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: str
    birth_date: date
    created_at: datetime
    is_active: bool

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    email: EmailStr
    password: str
