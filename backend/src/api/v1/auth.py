from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict
from src.database import engine
from src.models.user import UserCreate, User
from src.services.auth import authenticate_user, create_access_token, get_password_hash
from src.api.v1.models.auth import UserRegistration, UserLogin, TokenResponse

router = APIRouter()


@router.post("/register", response_model=Dict[str, str])
def register(user: UserRegistration):
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash the password
        hashed_password = get_password_hash(user.password)

        # Create new user
        db_user = User(email=user.email, hashed_password=hashed_password)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return {"message": "User created successfully"}


@router.post("/login", response_model=TokenResponse)
def login(user_credentials: UserLogin):
    with Session(engine) as session:
        user = authenticate_user(session, user_credentials.email, user_credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": user.id, "email": user.email})
        return TokenResponse(access_token=access_token, token_type="bearer")