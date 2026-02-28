from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") gettting error "ValueError: password cannot be longer than 72 bytes"
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash(password : str):
    return pwd_context.hash(password)


def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)