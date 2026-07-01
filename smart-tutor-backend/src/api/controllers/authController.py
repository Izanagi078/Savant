from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
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

class UpdateProfileSchema(BaseModel):
    full_name: str | None = None
    password: str | None = None

# Regex email validation helper
def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

# Password complexity verification helper
def check_password_complexity(password: str):
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long."
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one uppercase letter."
        )
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one lowercase letter."
        )
    if not re.search(r"[0-9]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one digit."
        )
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one special character (!@#$%^&* etc.)."
        )

@router.put("/update", response_model=UserResponseSchema)
async def update_profile(
    payload: UpdateProfileSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if payload.full_name is not None:
        current_user.full_name = payload.full_name
    if payload.password is not None and payload.password.strip():
        check_password_complexity(payload.password)
        current_user.hashed_password = hash_password(payload.password)
    
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def signup(
    payload: UserRegisterSchema,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    email_clean = payload.email.strip().lower()
    if not is_valid_email(email_clean):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a valid email address."
        )
    
    # Enforce password rules on registration
    check_password_complexity(payload.password)

    # Check if email is already taken
    result = await db.execute(select(User).filter(User.email == email_clean))
    existing_user = result.scalars().first()
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
    await db.commit()
    await db.refresh(new_user)
    
    # Set HttpOnly cookie for automatic login after signup
    access_token = create_access_token(data={"sub": new_user.email})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=3600 * 24,  # 24 hours
        path="/"
    )
    
    return new_user

@router.post("/login")
async def login(
    payload: UserLoginSchema,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    email_clean = payload.email.strip().lower()
    result = await db.execute(select(User).filter(User.email == email_clean))
    user = result.scalars().first()
    
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )
        
    access_token = create_access_token(data={"sub": user.email})
    
    # Issue HTTPOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=3600 * 24,  # 24 hours
        path="/"
    )
    
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    }

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/"
    )
    return {"detail": "Logged out successfully"}

@router.get("/me", response_model=UserResponseSchema)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
