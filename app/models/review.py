from sqlalchemy import Column, Integer, ForeignKey, Integer, Text, DateTime, func, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False, unique=True)  # ← one review per booking
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # DB-level constraint: rating must be 1–5
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_check'),
    )

    # Relationships
    booking = relationship("Booking", back_populates="review")
    user = relationship("User", secondary="bookings", viewonly=True, uselist=False)