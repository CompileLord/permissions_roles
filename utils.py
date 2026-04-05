from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password(password: str):
    return pwd_context.hash(password)

def verify_password(original_password: str, hashed_password: str):
    return pwd_context.verify(original_password, hashed_password)