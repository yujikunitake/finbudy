from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.users import UserCreate, UserRead
from app.database.repository.users_repository import UsersRepository
from app.core.security import verify_password
from app.core.jwt import create_access_token

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate):
    repo = UsersRepository()
    try:
        new_user = repo.create_user(user)
        return new_user
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao criar usuário: {e}.")
    

@users_router.post("/login", status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    repo = UsersRepository()
    user = repo.get_user_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário ou senha incorretos.")
    
    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token, 
        "token_type": "bearer"
    }
