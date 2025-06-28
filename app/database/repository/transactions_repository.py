from app.database.configs.connection import PostgresConnectionHandler
from app.database.entities.transactions import Transactions
from app.schemas.transactions import TransactionCreate


class TransactionsRepository:
    def create_transaction(self, user_id: int, transaction: TransactionCreate):
        with PostgresConnectionHandler() as db:
            try:
                new_transaction = Transactions(
                    user_id=user_id,
                    type=transaction.type,
                    value=transaction.value,
                    date=transaction.value,
                    description=transaction.description
                )

                db.session.add(new_transaction)
                db.session.commit()
                db.session.refresh(new_transaction)

                return new_transaction

            except Exception as e:
                db.session.rollback()
                raise Exception(f"Erro ao criar usuário: {str(e)}")
