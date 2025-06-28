from app.database.configs.base import Base
from app.database.entities.enums import TransactionType
from sqlalchemy import Column, Numeric, Integer, Enum, ForeignKey, Date, Text, DateTime, func



class Transactions(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Enum(TransactionType, name="transaction_type"), nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"Transactions[user_id={self.user_id}, type={self.type}, value={self.value}]"
    