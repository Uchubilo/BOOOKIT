from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.booking import booking_repo
from app.repositories.service import service_repo
from app.schemas.booking import BookingCreate, BookingUpdate
from app import models

class BookingService:
    def create_booking(self, db: Session, *, booking_in: BookingCreate, current_user: User):
        # 1. Validate service exists and is active
        service = service_repo.get(db, id=booking_in.service_id)
        if not service or not service.is_active:
            raise HTTPException(status_code=400, detail="Service not available")

        # 2. Validate start_time is in future
        if booking_in.start_time <= datetime.utcnow():
            raise HTTPException(status_code=400, detail="Start time must be in the future")

        # 3. Calculate end_time
        end_time = booking_in.start_time + timedelta(minutes=service.duration_minutes)

        # 4. Check for overlap
        if booking_repo.has_overlap(
            db,
            user_id=current_user.id,
            start_time=booking_in.start_time,
            end_time=end_time
        ):
            raise HTTPException(status_code=409, detail="Booking time slot unavailable due to overlap")

        # 5. Create booking
        booking = booking_repo.create(
            db,
            obj_in=booking_in,
            user_id=current_user.id,
            end_time=end_time
        )
        return booking

    def get_bookings(self, db: Session, *, current_user: User, status: str = None, start_from: datetime = None, start_to: datetime = None):
        if current_user.role == "admin":
            return booking_repo.get_all_with_filters(
                db, status=status, start_from=start_from, start_to=start_to
            )
        else:
            return booking_repo.get_by_user(db, user_id=current_user.id)

    def get_booking(self, db: Session, *, id: int, current_user: User):
        booking = booking_repo.get(db, id=id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        if booking.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=404, detail="Booking not found")  # avoid leaking info
        return booking

    def update_booking(self, db: Session, *, id: int, booking_in: BookingUpdate, current_user: User):
        booking = self.get_booking(db, id=id, current_user=current_user)

        if current_user.role == "admin":
            # Admin can update status freely
            if booking_in.status is not None:
                if booking_in.status not in ["pending", "confirmed", "cancelled", "completed"]:
                    raise HTTPException(status_code=400, detail="Invalid status")
                booking.status = booking_in.status
                db.commit()
                db.refresh(booking)
            return booking

        else:
            # User can only cancel or reschedule if pending/confirmed
            if booking.status not in ["pending", "confirmed"]:
                raise HTTPException(status_code=403, detail="Cannot modify completed or cancelled booking")

            if booking_in.status == "cancelled":
                booking.status = "cancelled"
                db.commit()
                db.refresh(booking)
                return booking

            if booking_in.start_time:
                # Reschedule
                service = service_repo.get(db, id=booking.service_id)
                new_end = booking_in.start_time + timedelta(minutes=service.duration_minutes)
                if booking_repo.has_overlap(
                    db,
                    user_id=current_user.id,
                    start_time=booking_in.start_time,
                    end_time=new_end,
                    exclude_booking_id=booking.id
                ):
                    raise HTTPException(status_code=409, detail="New time slot unavailable")
                booking.start_time = booking_in.start_time
                booking.end_time = new_end
                db.commit()
                db.refresh(booking)
            return booking

    def delete_booking(self, db: Session, *, id: int, current_user: User):
        booking = self.get_booking(db, id=id, current_user=current_user)

        if current_user.role == "admin":
            # Hard delete only if no review exists
            from app.repositories.review import review_repo
            if review_repo.get_by_booking(db, booking_id=booking.id):
                raise HTTPException(status_code=409, detail="Cannot delete booking with reviews")
            booking_repo.remove(db, id=id)
            return

        else:
            # User: only if start_time > now
            if booking.start_time <= datetime.utcnow():
                raise HTTPException(status_code=403, detail="Cannot delete past booking")
            booking.status = "cancelled"
            db.commit()

booking_service = BookingService()