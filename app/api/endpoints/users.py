from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, models, schemas, dependencies
from app.database import SessionLocal
from app.dependencies import get_current_user, get_current_admin, get_password_hash

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password,
        role_id=user.role_id,
        is_send_notify=user.is_send_notify
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db),
              current_user: models.User = Depends(get_current_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=schemas.ResponseWrapper[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 10,
    full_name: Optional[str] = None,
    email: Optional[str] = None,
    role_id: Optional[int] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    users = crud.get_users(db, skip=skip, limit=limit, full_name=full_name, email=email, role_id=role_id, sort_by=sort_by)
    count = len(users)

    response = schemas.ResponseWrapper(
        data=users,
        meta=schemas.Meta(count=count)
    )

    return response

@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int = Path(..., description="ID of the user to delete"),
                db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

@router.patch("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate,
                db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)
):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user