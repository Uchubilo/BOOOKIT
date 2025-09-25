from fastapi import APIRouter, Depends, status, Query
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from app.schemas.booking import BookingCreate, BookingUpdate, BookingOut, BookingConflict
from app.services.booking_service import booking_service
from app.models.user import User

router = APIRouter()

@router.post(
    "/",
    response_model=BookingOut,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"model": BookingConflict}}
)
def create_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return booking_service.create_booking(db, booking_in=booking_in, current_user=current_user)

@router.get("/", response_model=list[BookingOut])
def read_bookings(
    status: str = None,
    start_from: datetime = None,
    start_to: datetime = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return booking_service.get_bookings(
        db,
        current_user=current_user,
        status=status,
        start_from=start_from,
        start_to=start_to
    )

@router.get("/{id}", response_model=BookingOut)
def read_booking(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return booking_service.get_booking(db, id=id, current_user=current_user)

@router.patch("/{id}", response_model=BookingOut)
def update_booking(
    id: int,
    booking_in: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return booking_service.update_booking(db, id=id, booking_in=booking_in, current_user=current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking_service.delete_booking(db, id=id, current_user=current_user)
    return