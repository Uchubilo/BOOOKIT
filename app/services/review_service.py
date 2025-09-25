from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.review import review_repo
from app.repositories.booking import booking_repo
from app.schemas.review import ReviewCreate, ReviewUpdate

class ReviewService:
    def create_review(self, db: Session, *, review_in: ReviewCreate, current_user: User):
        # 1. Get booking
        booking = booking_repo.get(db, id=review_in.booking_id)
        if not booking:
            raise HTTPException(status_code=400, detail="Booking not found")

        # 2. Must belong to user
        if booking.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not your booking")

        # 3. Must be completed
        if booking.status != "completed":
            raise HTTPException(status_code=400, detail="Can only review completed bookings")

        # 4. Only one review allowed
        existing = review_repo.get_by_booking(db, booking_id=review_in.booking_id)
        if existing:
            raise HTTPException(status_code=400, detail="Review already exists for this booking")

        # 5. Create
        return review_repo.create(db, obj_in=review_in, user_id=current_user.id)

    def get_reviews_for_service(self, db: Session, *, service_id: int):
        return review_repo.get_by_service(db, service_id=service_id)

    def update_review(self, db: Session, *, id: int, review_in: ReviewUpdate, current_user: User):
        review = review_repo.get(db, id=id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        # Get booking to check ownership
        booking = booking_repo.get(db, id=review.booking_id)
        if booking.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not your review")
        return review_repo.update(db, db_obj=review, obj_in=review_in)

    def delete_review(self, db: Session, *, id: int, current_user: User):
        review = review_repo.get(db, id=id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        booking = booking_repo.get(db, id=review.booking_id)
        if booking.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Not your review")
        review_repo.remove(db, id=id)

review_service = ReviewService()