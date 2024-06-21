from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app import models, schemas

# def get_car(db: Session, car_id: int):
#     return db.query(models.Car).filter(models.Car.id == car_id).first()
#
# def get_cars(db: Session, skip: int = 0, limit: int = 100, model: str = None, brand: str = None, sort_by: str = None):
#     query = db.query(models.Car)
#     if model:
#         query = query.filter(models.Car.model == model)
#     if brand:
#         query = query.filter(models.Car.brand == brand)
#     if sort_by:
#         if sort_by.startswith('-'):
#             query = query.order_by(desc(sort_by[1:]))
#         else:
#             query = query.order_by(asc(sort_by))
#     return query.offset(skip).limit(limit).all()

# def create_car(db: Session, car: schemas.CarCreate):
#     db_car = models.Car(**car.dict())
#     db.add(db_car)
#     db.commit()
#     db.refresh(db_car)
#     return db_car
#
# def delete_car(db: Session, car_id: int):
#     db_car = db.query(models.Car).filter(models.Car.id == car_id).first()
#     if db_car is None:
#         return None
#     db.delete(db_car)
#     db.commit()
#     return db_car
#
# def update_car(db: Session, car_id: int, car: schemas.CarUpdate):
#     db_car = db.query(models.Car).filter(models.Car.id == car_id).first()
#     if db_car is None:
#         return None
#     for key, value in car.dict().items():
#         setattr(db_car, key, value)
#     db.commit()
#     db.refresh(db_car)
#     return db_car

def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def get_services(db: Session, skip: int = 0, limit: int = 100, name: str = None, sort_by: str = None):
    query = db.query(models.Service)
    if name:
        query = query.filter(models.Service.name == name)
    if sort_by:
        if sort_by.startswith('-'):
            query = query.order_by(desc(sort_by[1:]))
        else:
            query = query.order_by(asc(sort_by))
    return query.offset(skip).limit(limit).all()

def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def delete_service(db: Session, service_id: int):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service:
        db.delete(db_service)
        db.commit()
    return db_service

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100, full_name: str = None, email: str = None, role_id: int = None, sort_by: str = None):
    query = db.query(models.User)
    if full_name:
        query = query.filter(models.User.full_name == full_name)
    if email:
        query = query.filter(models.User.email == email)
    if role_id is not None:
        query = query.filter(models.User.role_id == role_id)
    if sort_by:
        if sort_by.startswith('-'):
            query = query.order_by(desc(sort_by[1:]))
        else:
            query = query.order_by(asc(sort_by))
    return query.offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def get_customer_car(db: Session, customer_car_id: int):
    return db.query(models.CustomerCar).filter(models.CustomerCar.id == customer_car_id).first()

def get_customer_cars(db: Session, skip: int = 0, limit: int = 100, year: int = None, number: str = None, user_id: int = None, car_id: int = None, sort_by: str = None):
    query = db.query(models.CustomerCar)
    if year:
        query = query.filter(models.CustomerCar.year == year)
    if number:
        query = query.filter(models.CustomerCar.number == number)
    if user_id is not None:
        query = query.filter(models.CustomerCar.user_id == user_id)
    if car_id is not None:
        query = query.filter(models.CustomerCar.car_id == car_id)
    if sort_by:
        if sort_by.startswith('-'):
            query = query.order_by(desc(sort_by[1:]))
        else:
            query = query.order_by(asc(sort_by))
    return query.offset(skip).limit(limit).all()

def create_customer_car(db: Session, customer_car: schemas.CustomerCarCreate):
    db_customer_car = models.CustomerCar(**customer_car.dict())
    db.add(db_customer_car)
    db.commit()
    db.refresh(db_customer_car)
    return db_customer_car

def delete_customer_car(db: Session, customer_car_id: int):
    db_customer_car = db.query(models.CustomerCar).filter(models.CustomerCar.id == customer_car_id).first()
    if db_customer_car:
        db.delete(db_customer_car)
        db.commit()
    return db_customer_car

def update_customer_car(db: Session, customer_car_id: int, customer_car: schemas.CustomerCarUpdate):
    db_customer_car = db.query(models.CustomerCar).filter(models.CustomerCar.id == customer_car_id).first()
    if db_customer_car is None:
        return None
    for key, value in customer_car.dict().items():
        setattr(db_customer_car, key, value)
    db.commit()
    db.refresh(db_customer_car)
    return db_customer_car

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100, status: int = None, user_id: int = None, customer_car_id: int = None, sort_by: str = None):
    query = db.query(models.Order)
    if status is not None:
        query = query.filter(models.Order.status == status)
    if user_id is not None:
        query = query.filter(models.Order.user_id == user_id)
    if customer_car_id is not None:
        query = query.filter(models.Order.customer_car_id == customer_car_id)
    if sort_by:
        if sort_by.startswith('-'):
            query = query.order_by(desc(sort_by[1:]))
        else:
            query = query.order_by(asc(sort_by))
    return query.offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order