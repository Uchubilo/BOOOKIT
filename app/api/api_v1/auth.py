from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.db.session import get_db
from app.core.config import settings
from app.core.deps import oauth2_scheme
from app.schemas.user import UserCreate
from app.schemas.auth import Token
from app.services.auth_service import auth_service

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_and_login(db, user_in=user_in)

# Add this method to AuthService (we'll update it below)