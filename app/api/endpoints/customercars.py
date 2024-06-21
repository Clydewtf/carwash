from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, models, schemas
from app.database import SessionLocal
from app.dependencies import get_current_user, get_current_admin

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.CustomerCar)
def create_customer_car(customer_car: schemas.CustomerCarCreate, db: Session = Depends(get_db),
                        current_user: models.User = Depends(get_current_admin)):
    return crud.create_customer_car(db=db, customer_car=customer_car)

@router.get("/{customer_car_id}", response_model=schemas.CustomerCar)
def read_customer_car(customer_car_id: int, db: Session = Depends(get_db),
                      current_user: models.User = Depends(get_current_user)):
    db_customer_car = crud.get_customer_car(db, customer_car_id=customer_car_id)
    if db_customer_car is None:
        raise HTTPException(status_code=404, detail="CustomerCar not found")
    return db_customer_car

@router.get("/", response_model=schemas.ResponseWrapper[schemas.CustomerCar])
def read_customer_cars(
    skip: int = 0,
    limit: int = 10,
    year: Optional[int] = None,
    number: Optional[str] = None,
    user_id: Optional[int] = None,
    car_id: Optional[int] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    customer_cars = crud.get_customer_cars(db, skip=skip, limit=limit, year=year, number=number, user_id=user_id, car_id=car_id, sort_by=sort_by)
    count = len(customer_cars)

    response = schemas.ResponseWrapper(
        data=customer_cars,
        meta=schemas.Meta(count=count)
    )

    return response

@router.delete("/{customer_car_id}", response_model=schemas.CustomerCar)
def delete_customer_car(customer_car_id: int = Path(..., description="ID of the customercar to delete"),
                        db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    db_customer_car = crud.get_customer_car(db, customer_car_id=customer_car_id)
    if db_customer_car is None:
        raise HTTPException(status_code=404, detail="CustomerCar not found")
    db.delete(db_customer_car)
    db.commit()
    return db_customer_car

@router.put("/{customer_car_id}", response_model=schemas.CustomerCar)
def update_customer_car(customer_car_id: int, customer_car: schemas.CustomerCarUpdate,
                        db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)
):
    db_customer_car = crud.update_customer_car(db=db, customer_car_id=customer_car_id, customer_car=customer_car)
    if db_customer_car is None:
        raise HTTPException(status_code=404, detail="CustomerCar not found")
    return db_customer_car