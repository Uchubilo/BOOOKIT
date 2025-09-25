from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from decimal import Decimal
from app.db.session import get_db
from app.core.deps import get_current_user, require_admin
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceOut
from app.services.service_service import service_service
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[ServiceOut])
def read_services(
    q: str = None,
    price_min: Decimal = None,
    price_max: Decimal = None,
    active: bool = True,
    db: Session = Depends(get_db)
):
    return service_service.get_services(
        db, q=q, price_min=price_min, price_max=price_max, active=active
    )

@router.get("/{id}", response_model=ServiceOut)
def read_service(id: int, db: Session = Depends(get_db)):
    return service_service.get_service(db, id=id)

@router.post("/", response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
def create_service(
    service_in: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return service_service.create_service(db, service_in=service_in, current_user=current_user)

@router.patch("/{id}", response_model=ServiceOut)
def update_service(
    id: int,
    service_in: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return service_service.update_service(db, id=id, service_in=service_in, current_user=current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    service_service.delete_service(db, id=id, current_user=current_user)
    return