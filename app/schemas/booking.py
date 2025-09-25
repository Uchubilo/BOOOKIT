from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class BookingBase(BaseModel):
    service_id: int
    start_time: datetime

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    status: Optional[str] = None  # Only admin can set arbitrary status

class BookingOut(BaseModel):
    id: int
    user_id: int
    service_id: int
    start_time: datetime
    end_time: datetime
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# For conflict response
class BookingConflict(BaseModel):
    detail: str = "Booking time slot unavailable due to overlap"