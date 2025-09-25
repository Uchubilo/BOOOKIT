from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.service import Service
from app.repositories.base import BaseRepository
from app.schemas.service import ServiceCreate, ServiceUpdate

class ServiceRepository(BaseRepository[Service]):
    def get_active(self, db: Session) -> List[Service]:
        return db.query(Service).filter(Service.is_active == True).all()

    def search(
        self,
        db: Session,
        *,
        q: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        active: bool = True
    ) -> List[Service]:
        query = db.query(Service).filter(Service.is_active == active)
        if q:
            query = query.filter(
                or_(
                    Service.title.ilike(f"%{q}%"),
                    Service.description.ilike(f"%{q}%")
                )
            )
        if price_min is not None:
            query = query.filter(Service.price >= price_min)
        if price_max is not None:
            query = query.filter(Service.price <= price_max)
        return query.all()

service_repo = ServiceRepository(Service)