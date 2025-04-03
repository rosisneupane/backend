from fastapi import Depends, HTTPException,Request
from fastapi.security import OAuth2PasswordBearer
from utils.security import decode_access_token
from utils.security import decode_access_token_admin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    print(payload)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload["sub"]
 

def get_current_user_admin(request: Request):
    token = request.cookies.get("admin_token")  # Extract token from cookies
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    payload = decode_access_token_admin(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload["sub"]


