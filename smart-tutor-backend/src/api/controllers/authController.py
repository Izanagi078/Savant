from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import re
from src.config.dbConfig import get_db
from src.models.user import User
from src.services.authService import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

class UserRegisterSchema(BaseModel):
    email: str
    password: str
    full_name: str | None = None

class UserLoginSchema(BaseModel):
    email: str
    password: str

class UserResponseSchema(BaseModel):
    id: int
    email: str
    full_name: str | None
    
    class Config:
        from_attributes = True

# Simple regex validation helper to protect email structure without email-validator package dependency
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))

@router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def signup(payload: UserRegisterSchema, db: Session = Depends(get_db)):
    email_clean = payload.email.strip().lower()
    if not is_valid_email(email_clean):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a valid email address."
        )
    if len(payload.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long."
        )

    # Check if email is already taken
    existing_user = db.query(User).filter(User.email == email_clean).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists."
        )
        
    new_user = User(
        email=email_clean,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(payload: UserLoginSchema, db: Session = Depends(get_db)):
    email_clean = payload.email.strip().lower()
    user = db.query(User).filter(User.email == email_clean).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )
        
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    }

@router.get("/me", response_model=UserResponseSchema)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
