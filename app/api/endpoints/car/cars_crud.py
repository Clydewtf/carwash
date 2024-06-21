from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app import models, schemas
from app.api.endpoints.car import cars_schemas

def get_car(db: Session, car_id: int):
    return db.query(models.Car).filter(models.Car.id == car_id).first()

def get_cars(db: Session, skip: int = 0, limit: int = 100, model: str = None, brand: str = None, sort_by: str = None):
    query = db.query(models.Car)
    if model:
        query = query.filter(models.Car.model == model)
    if brand:
        query = query.filter(models.Car.brand == brand)
    if sort_by:
        if sort_by.startswith('-'):
            query = query.order_by(desc(sort_by[1:]))
        else:
            query = query.order_by(asc(sort_by))
    return query.offset(skip).limit(limit).all()

def create_car(db: Session, car: cars_schemas.CarCreate):
    db_car = models.Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def delete_car(db: Session, car_id: int):
    db_car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if db_car is None:
        return None
    db.delete(db_car)
    db.commit()
    return db_car

def update_car(db: Session, car_id: int, car: cars_schemas.CarUpdate):
    db_car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if db_car is None:
        return None
    for key, value in car.dict().items():
        setattr(db_car, key, value)
    db.commit()
    db.refresh(db_car)
    return db_car