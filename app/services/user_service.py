from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user import user_repo
from app.schemas.user import UserUpdate

class UserService:
    def get_me(self, current_user: User):
        return current_user

    def update_me(self, db: Session, *, current_user: User, user_in: UserUpdate):
        # Check email uniqueness if updating email
        if user_in.email and user_in.email != current_user.email:
            existing = user_repo.get_by_email(db, email=user_in.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already taken"
                )
        user = user_repo.update(db, db_obj=current_user, obj_in=user_in)
        return user

user_service = UserService()

