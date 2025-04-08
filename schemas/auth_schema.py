from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from schemas.user_schema import UserResponse





class UserCreate(BaseModel):
    name: str
    email: str



class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    guardianEmail: str
    guardianPhone: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class OTPVerificationRequest(BaseModel):
    email: str
    otp: str

class TestPayload(BaseModel):
    username: str
    email: str
    password: str
    guardianEmail: str
    guardianPhone: str