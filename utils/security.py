from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from uuid import UUID



SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool: 
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    # Convert UUID to string before encoding
    if "sub" in to_encode and isinstance(to_encode["sub"], UUID):
        to_encode["sub"] = str(to_encode["sub"])

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)

        # Convert the 'sub' field back to UUID if it's a valid string representation of a UUID
        if "sub" in payload:
            payload["sub"] = UUID(payload["sub"])

        return payload
    except JWTError:
        return None
    

def decode_access_token_admin(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Convert 'sub' field back to UUID if applicable
        if "sub" in payload:
            try:
                payload["sub"] = UUID(payload["sub"])
            except ValueError:
                return None  # Invalid UUID format
        
        # Ensure 'is_admin' is present and True
        if not payload.get("is_admin", False):
            return None
        
        return payload
    except JWTError:
        return None