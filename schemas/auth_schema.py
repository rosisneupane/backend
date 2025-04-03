from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    guardianEmail: str
    guardianPhone: str
    is_verified: bool
    verification_otp:Optional[str]
    is_admin:bool



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

class OTPVerificationRequest(BaseModel):
    email: str
    otp: str

class TestPayload(BaseModel):
    username: str
    email: str
    password: str
    guardianEmail: str
    guardianPhone: str