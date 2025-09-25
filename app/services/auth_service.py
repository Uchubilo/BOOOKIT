from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user import user_repo
from app.schemas.user import UserCreate
from app.schemas.auth import Token
from app.core.security import verify_password, create_access_token, create_refresh_token

class AuthService:
    def register(self, db: Session, *, user_in: UserCreate):
        # Check email uniqueness
        if user_repo.get_by_email(db, email=user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        user = user_repo.create(db, obj_in=user_in)
        return user

    def login(self, db: Session, *, email: str, password: str) -> Token:
        user = user_repo.get_by_email(db, email=email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, refresh_token=refresh_token)

    def refresh_token(self, user_id: str) -> str:
        return create_access_token(data={"sub": user_id})
    
    def register_and_login(self, db: Session, *, user_in: UserCreate) -> Token:
        self.register(db, user_in=user_in)
        return self.login(db, email=user_in.email, password=user_in.password)

auth_service = AuthService()