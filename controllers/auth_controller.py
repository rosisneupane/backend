from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse,UserResponse,OTPVerificationRequest,TestPayload
from models.user_model import User
from database.database import get_db
from utils.security import hash_password, verify_password, create_access_token
from utils.email_sender import send_verification_email
from utils.otp import generate_otp
from typing import List
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])
 


@router.get("/users/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/users/me", response_model=UserResponse)
def get_user_details(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.post("/auth/register", response_model=UserResponse)
def register_user(user: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pwd = hash_password(user.password)
    verification_otp = generate_otp()

    db_user = User(
        username=user.username, 
        email=user.email,
        guardianEmail=user.guardianEmail,
        guardianPhone=user.guardianPhone,
        is_verified=False,
        verification_otp=verification_otp,
        hashed_password=hashed_pwd
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    print("Registered user:", db_user.email, "OTP:", db_user.verification_otp)
    send_verification_email(user.guardianEmail, verification_otp)

    return db_user



@router.post("/auth/verify-otp", response_model=TokenResponse)
def verify_otp(payload: OTPVerificationRequest, db: Session = Depends(get_db)):
    print(f"🔹 Verifying OTP for guardian email: {payload.email}")

    # Find user by guardianEmail instead of user email
    user = db.query(User).filter(User.guardianEmail == payload.email).first()

    if not user:
        print(f"❌ No user found with guardian email {payload.email} in the database!")
        all_users = db.query(User).all()
        print(f"🔍 All Registered Users: {[u.guardianEmail for u in all_users]}")  # Print all guardian emails
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        print("⚠️ User is already verified")
        raise HTTPException(status_code=400, detail="User already verified")

    if user.verification_otp != payload.otp:
        print("❌ Invalid OTP!")
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # If OTP matches, mark user as verified
    user.is_verified = True
    user.verification_otp = None  # Clear OTP after verification
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": user.id})

    print("✅ OTP verified successfully using guardian email!")
    return {"access_token": token, "token_type": "bearer"}



# @router.post("/auth/login", response_model=TokenResponse)
# def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == credentials.username).first()
#     if not user or not verify_password(credentials.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token(data={"sub": user.username})
#     return {"access_token": token, "token_type": "bearer"}

@router.post("/auth/login", response_model=TokenResponse)
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        # Regenerate OTP (optional) or re-use the existing one
        otp = user.verification_otp
        if not otp:
            otp = generate_otp()
            user.verification_otp = otp
            db.commit()

        send_verification_email(user.email, otp)
        return {"detail": "User not verified. OTP has been sent to your email.", "email": user.email}
    
    # User is verified, issue token
    token = create_access_token(data={"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}

