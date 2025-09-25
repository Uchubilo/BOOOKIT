from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user, require_admin
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewOut
from app.services.review_service import review_service
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return review_service.create_review(db, review_in=review_in, current_user=current_user)

@router.get("/services/{service_id}", response_model=list[ReviewOut])
def read_reviews_for_service(service_id: int, db: Session = Depends(get_db)):
    return review_service.get_reviews_for_service(db, service_id=service_id)

@router.patch("/{id}", response_model=ReviewOut)
def update_review(
    id: int,
    review_in: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return review_service.update_review(db, id=id, review_in=review_in, current_user=current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review_service.delete_review(db, id=id, current_user=current_user)
    return