from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.review import Review
from app.models.booking import Booking
from app.repositories.base import BaseRepository
from app.schemas.review import ReviewCreate

class ReviewRepository(BaseRepository[Review]):
    def get_by_booking(self, db: Session, *, booking_id: int) -> Optional[Review]:
        return db.query(Review).filter(Review.booking_id == booking_id).first()

    def get_by_service(self, db: Session, *, service_id: int) -> List[Review]:
        return (
            db.query(Review)
            .join(Review.booking)
            .filter(Booking.service_id == service_id)
            .all()
        )

    def create(self, db: Session, *, obj_in: ReviewCreate, user_id: int) -> Review:
        # Note: We assume booking ownership is validated in service layer
        db_obj = Review(
            booking_id=obj_in.booking_id,
            rating=obj_in.rating,
            comment=obj_in.comment
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

review_repo = ReviewRepository(Review)