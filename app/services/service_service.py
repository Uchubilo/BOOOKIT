from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.service import service_repo
from app.schemas.service import ServiceCreate, ServiceUpdate

class ServiceService:
    def get_services(
        self,
        db: Session,
        *,
        q: str = None,
        price_min: float = None,
        price_max: float = None,
        active: bool = True
    ):
        return service_repo.search(
            db, q=q, price_min=price_min, price_max=price_max, active=active
        )

    def get_service(self, db: Session, *, id: int):
        service = service_repo.get(db, id=id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        return service

    def create_service(self, db: Session, *, service_in: ServiceCreate, current_user: User):
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return service_repo.create(db, obj_in=service_in)

    def update_service(self, db: Session, *, id: int, service_in: ServiceUpdate, current_user: User):
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Not enough permissions")
        service = service_repo.get(db, id=id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        return service_repo.update(db, db_obj=service, obj_in=service_in)

    def delete_service(self, db: Session, *, id: int, current_user: User):
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Not enough permissions")
        service = service_repo.get(db, id=id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        # Soft delete: mark as inactive
        service.is_active = False
        db.commit()
        return service

service_service = ServiceService()