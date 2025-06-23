from app.database.configs.connection import PostgresConnectionHandler
from app.database.entities.users import Users
from app.schemas.users import UserCreate
from app.core.security import get_password_hash


class UsersRepository:
    def create_user(self, user: UserCreate):
        with PostgresConnectionHandler() as db:
            try:
                existing_user = db.session.query(Users).filter(Users.email == user.email).first()
                if existing_user:
                    raise ValueError("E-mail já cadastrado.")
                
                hashed_password = get_password_hash(user.password)

                insert_data = Users(
                    email=user.email,
                    password=hashed_password,
                    name=user.name,
                    birth_date=user.birth_date
                )

                db.session.add(insert_data)
                db.session.commit()
                db.session.refresh(insert_data)
                
                return insert_data
            
            except Exception as e:
                db.session.rollback()
                raise Exception(f"Erro ao criar usuário: {str(e)}")
            
    def get_user_by_email(self, email: str) -> Users | None:
        with PostgresConnectionHandler() as db:
            try:
                return db.session.query(Users).filter(Users.email == email).first()
            except Exception as e:
                db.session.rollback()
                raise Exception(f"Erro ao realizar login: {str(e)}")