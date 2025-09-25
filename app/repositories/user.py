from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate

class UserRepository(BaseRepository[User]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(func.lower(User.email) == func.lower(email)).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        from app.core.security import get_password_hash
        db_obj = User(
            name=obj_in.name,
            email=obj_in.email,
            password_hash=get_password_hash(obj_in.password),
            role="user"
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            # Not handled here — password change would be separate
            del update_data["password"]
        if "email" in update_data:
            update_data["email"] = update_data["email"].lower()
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

user_repo = UserRepository(User)