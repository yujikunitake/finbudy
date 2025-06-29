from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import date
from app.schemas.transactions import TransactionCreate, TransactionRead, TransactionUpdate, BalanceRead
from app.database.entities.enums import TransactionType
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


@transactions_router.get("/transactions", response_model=List[TransactionRead], status_code=status.HTTP_200_OK)
def list_transaction(
    user_id: int =  Depends(get_current_user),
    type:  Optional[TransactionType] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    description: Optional[str] = None
):
    repo = TransactionsRepository()
    try:
        transactions = repo.get_transactions_filtered(
            user_id=user_id,
            type=type,
            start_date=start_date,
            end_date=end_date,
            min_value=min_value,
            max_value=max_value,
            description=description
        )

        return transactions
    
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except SQLAlchemyError as sqle:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(sqle))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@transactions_router.patch("/{transaction_id}", response_model=TransactionRead, status_code=status.HTTP_200_OK)
def update_transaction(
    transaction_id: int,
    updates: TransactionUpdate,
    user_id: int = Depends(get_current_user)
):
    repo = TransactionsRepository()
    try:
        updated_transaction = repo.update_transaction(transaction_id, user_id, updates)

        return updated_transaction
    
    except ValueError as vc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(vc))
    except SQLAlchemyError as sqle:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(sqle))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@transactions_router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    user_id: int = Depends(get_current_user)
):
    repo = TransactionsRepository()
    try:
        repo.delete_transaction(transaction_id, user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except SQLAlchemyError as sqle:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(sqle))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@transactions_router.get("/balance", response_model=BalanceRead, status_code=status.HTTP_200_OK)
def get_balance(user_id: int = Depends(get_current_user)):
    repo = TransactionsRepository()
    try:
        balance = repo.get_balance(user_id)

        return balance
    
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except SQLAlchemyError as sqle:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(sqle))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
