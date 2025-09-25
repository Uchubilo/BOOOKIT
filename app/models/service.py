from sqlalchemy import Column, Integer, String, Text, Numeric, Integer, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)  # e.g., 99.99
    duration_minutes = Column(Integer, nullable=False)  # e.g., 60
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    bookings = relationship("Booking", back_populates="service", cascade="all, delete-orphan")