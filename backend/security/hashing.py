from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Hash + salt intégré avec passlib
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#Verif
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
