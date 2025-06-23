from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Gera hash a partir de uma senha em texto puro."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara senha em texto puro com hash."""
    return pwd_context.verify(plain_password, hashed_password)
