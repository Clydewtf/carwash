from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, models, schemas
from app.database import SessionLocal
from app.dependencies import get_current_user, get_current_admin
from app.api.endpoints.car import cars_crud, cars_schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=cars_schemas.Car)
def create_car(car: cars_schemas.CarCreate, db: Session = Depends(get_db),
               current_user: models.User = Depends(get_current_admin)):
    return cars_crud.create_car(db=db, car=car)

@router.get("/{car_id}", response_model=cars_schemas.Car)
def read_car(car_id: int, db: Session = Depends(get_db),
             current_user: models.User = Depends(get_current_user)):
    db_car = cars_crud.get_car(db, car_id=car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car

@router.get("/", response_model=schemas.ResponseWrapper[cars_schemas.Car])
def read_cars(
    skip: int = 0,
    limit: int = 10,
    model: Optional[str] = None,
    brand: Optional[str] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    cars = cars_crud.get_cars(db, skip=skip, limit=limit, model=model, brand=brand, sort_by=sort_by)
    count = len(cars)

    response = schemas.ResponseWrapper(
        data=cars,
        meta=schemas.Meta(count=count)
    )

    return response

@router.delete("/{car_id}", response_model=cars_schemas.Car)
def delete_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    db_car = cars_crud.delete_car(db=db, car_id=car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car

@router.put("/{car_id}", response_model=cars_schemas.Car)
def update_car(
    car_id: int,
    car: cars_schemas.CarUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    db_car = cars_crud.update_car(db=db, car_id=car_id, car=car)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car