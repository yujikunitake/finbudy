from app.database.configs.connection import PostgresConnectionHandler
from app.database.entities.transactions import Transactions
from app.schemas.transactions import TransactionCreate
from app.database.entities.enums import TransactionType
from datetime import date
from sqlalchemy.exc import SQLAlchemyError


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
