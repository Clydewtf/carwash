from pydantic import BaseModel
from typing import List, Optional, TypeVar, Generic, Type
from datetime import datetime

T = TypeVar("T")

class Meta(BaseModel):
    count: int

class ResponseWrapper(BaseModel, Generic[T]):
    data: List[T]
    meta: Meta

# class CarBase(BaseModel):
#     model: str
#     brand: str
#
# class CarCreate(CarBase):
#     pass
#
# class Car(CarBase):
#     id: int
#
#     class Config:
#         orm_mode = True
#
# class CarUpdate(BaseModel):
#     model: str
#     brand: str
#
#     class Config:
#         orm_mode = True

class ServiceBase(BaseModel):
    name: str
    price_in_cents: int
    duration_in_seconds: int

class ServiceCreate(BaseModel):
    name: str
    price_in_rubles: float
    duration_in_minutes: int

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    price_in_rubles: Optional[int] = None
    duration_in_minutes: Optional[int] = None

class Service(ServiceBase):
    id: int

    class Config:
        orm_mode = True

class PriceVO(BaseModel):
    minValue: int
    maxValue: float
    format: str

class TimeVO(BaseModel):
    second: int
    minute: int

class ServiceVO(BaseModel):
    id: int
    name: str
    price: PriceVO
    time: TimeVO

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    full_name: str
    email: str
    role_id: int
    is_send_notify: Optional[bool] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str

class UserUpdate(BaseModel):
    full_name: str
    email: str
    role_id: int
    is_send_notify: bool
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class CustomerCarBase(BaseModel):
    year: int
    number: str
    customer_id: int
    car_id: int

class CustomerCarCreate(CustomerCarBase):
    pass

class CustomerCar(CustomerCarBase):
    id: int

    class Config:
        orm_mode = True

class CustomerCarUpdate(BaseModel):
    year: int
    number: str
    customer_id: int
    car_id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    status: int

class OrderCreate(OrderBase):
    customer_car_id: int
    employee_id: int
    service_ids: List[int]

class OrderUpdateStatus(BaseModel):
    status: int

class Order(OrderBase):
    id: int
    start_date: datetime
    end_date: datetime
    total_time: int
    total_price: int
    administrator_id: int
    employee_id: int
    customer_car_id: int

    class Config:
        orm_mode = True

class OrderDetail(BaseModel):
    id: int
    status: int
    start_date: datetime
    end_date: datetime
    total_time: int
    total_price: int
    administrator: dict
    employee: dict
    customer_car: dict

    class Config:
        orm_mode = True