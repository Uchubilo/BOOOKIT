from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from app.schemas.user import UserOut, UserUpdate
from app.services.user_service import user_service
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return user_service.get_me(current_user)

@router.patch("/me", response_model=UserOut)
def update_users_me(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.update_me(db, current_user=current_user, user_in=user_in)