from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.booking import Booking
from app.repositories.base import BaseRepository
from app.schemas.booking import BookingCreate

class BookingRepository(BaseRepository[Booking]):
    def get_by_user(self, db: Session, *, user_id: int) -> List[Booking]:
        return db.query(Booking).filter(Booking.user_id == user_id).all()

    def get_all_with_filters(
        self,
        db: Session,
        *,
        status: Optional[str] = None,
        start_from: Optional[datetime] = None,
        start_to: Optional[datetime] = None
    ) -> List[Booking]:
        query = db.query(Booking)
        if status:
            query = query.filter(Booking.status == status)
        if start_from:
            query = query.filter(Booking.start_time >= start_from)
        if start_to:
            query = query.filter(Booking.start_time <= start_to)
        return query.all()

    def has_overlap(
        self,
        db: Session,
        *,
        user_id: int,
        start_time: datetime,
        end_time: datetime,
        exclude_booking_id: Optional[int] = None
    ) -> bool:
        query = db.query(Booking).filter(
            Booking.user_id == user_id,
            Booking.status.in_(["pending", "confirmed"]),
            or_(
                and_(Booking.start_time < end_time, Booking.end_time > start_time)
            )
        )
        if exclude_booking_id:
            query = query.filter(Booking.id != exclude_booking_id)
        return db.query(query.exists()).scalar()

    def create(self, db: Session, *, obj_in: BookingCreate, user_id: int, end_time: datetime) -> Booking:
        db_obj = Booking(
            user_id=user_id,
            service_id=obj_in.service_id,
            start_time=obj_in.start_time,
            end_time=end_time,
            status="pending"
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

booking_repo = BookingRepository(Booking)