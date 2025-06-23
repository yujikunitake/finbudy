from app.database.configs.base import Base
from sqlalchemy import Column, String, Integer, Date, DateTime, Boolean, func


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"Users [email={self.email}, name={self.name}, is_active={self.is_active}]"
