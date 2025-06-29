from app.database.configs.connection import PostgresConnectionHandler
from app.database.entities.transactions import Transactions
from app.schemas.transactions import TransactionCreate, TransactionUpdate
from app.database.entities.enums import TransactionType
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func


class TransactionsRepository:
    def create_transaction(self, user_id: int, transaction: TransactionCreate):
        with PostgresConnectionHandler() as db:
            try:
                new_transaction = Transactions(
                    user_id=user_id,
                    type=transaction.type.value,
                    value=transaction.value,
                    date=transaction.date,
                    description=transaction.description
                )

                db.session.add(new_transaction)
                db.session.commit()
                db.session.refresh(new_transaction)

                return new_transaction

            except SQLAlchemyError as sqle:
                db.session.rollback()
                raise Exception(f"Erro de banco de dados ao criar transação: {str(sqle)}")
            except Exception as e:
                db.session.rollback()
                raise Exception(f"Erro ao criar usuário: {str(e)}")
            
    def get_transactions_filtered(
            self,
            user_id: int,
            type: TransactionType = None,
            start_date: date = None,
            end_date: date = None,
            min_value: float = None,
            max_value: float = None,
            description: str = None
    ):
        with PostgresConnectionHandler() as db:
            try:
                query = db.session.query(Transactions).filter(Transactions.user_id == user_id)

                if type:
                    query = query.filter(Transactions.type == type.value)
                if start_date:
                    query = query.filter(Transactions.date >= start_date)
                if end_date:
                    query = query.filter(Transactions.date <= end_date)
                if min_value:
                    query = query.filter(Transactions.value >= min_value)
                if max_value:
                    query = query.filter(Transactions.value <= max_value)
                if description:
                    query = query.filter(Transactions.description.ilike(f"%{description}%"))

                return query.all()
            
            except SQLAlchemyError as sqle:
                db.session.rollback()
                raise Exception(f"Erro de banco de dados ao buscar transações: {str(sqle)}")
            except Exception as e:
                db.session.rollback()
                raise Exception(f"Erro ao consultar transações: {str(e)}")

    def update_transaction(self, transaction_id: int, user_id: int, updates: TransactionUpdate):
        with PostgresConnectionHandler() as db:
            try:
                transaction = db.session.query(Transactions).filter_by(id=transaction_id, user_id=user_id).first()

                if not transaction:
                    raise ValueError("Transação não localizada.")
                
                if updates.type is not None:
                    transaction.type = updates.type.value
                if updates.value is not None:
                    transaction.value = updates.value
                if updates.transaction_date is not None:
                    transaction.date = updates.transaction_date
                if updates.description is not None:
                    transaction.description = updates.description

                db.session.commit()
                db.session.refresh(transaction)

                return transaction

            except SQLAlchemyError as sqle:
                db.session.rollback()
                raise Exception(f"Erro de banco de dados ao editar transação: {str(sqle)}")
            except Exception as e:
                db.session.rollback()
                raise Exception(f"Erro ao atualizar transações: {str(e)}")

    def get_balance(self, user_id: int) -> float:
        with PostgresConnectionHandler() as db:
            try:
                income = db.session.query(
                    func.coalesce(func.sum(Transactions.value), 0)
                    ).filter_by(user_id=user_id, type=TransactionType.income.value).scalar()
                
                expense = db.session.query(
                    func.coalesce(func.sum(Transactions.value), 0)
                ).filter_by(user_id=user_id, type=TransactionType.expense.value).scalar()

                return {
                    "total_income": income,
                    "total_expense": expense,
                    "balance": income - expense
                }
            
            except SQLAlchemyError as sqle:
                db.session.rollback()
                raise Exception(f"Erro de banco de dados ao buscar saldo: {str(sqle)}")
            except Exception as e:
                db.session.rollback()
                raise Exception(f"Erro ao consultar transações: {str(e)}")
            