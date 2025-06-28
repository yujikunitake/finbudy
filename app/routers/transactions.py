from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.transactions import TransactionCreate, TransactionRead
from app.database.repository.transactions_repository import TransactionsRepository
from app.core.jwt import get_current_user

transactions_router = APIRouter(prefix="/transactions", tags=["transactions"])


@transactions_router.post("/register_transaction", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def register_transaction(
    transaction: TransactionCreate,
    user_id: int = Depends(get_current_user),
):
    repo = TransactionsRepository()
    try:
        new_transaction = repo.create_transaction(user_id, transaction)
        return new_transaction
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except SQLAlchemyError as sqle:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(sqle))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
