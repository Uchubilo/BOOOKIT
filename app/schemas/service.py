from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

class ServiceBase(BaseModel):
    title: str
    description: str
    price: Decimal
    duration_minutes: int
    is_active: Optional[bool] = True

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    duration_minutes: Optional[int] = None
    is_active: Optional[bool] = None

class ServiceOut(ServiceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True