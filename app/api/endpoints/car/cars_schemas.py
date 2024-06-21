from pydantic import BaseModel
from typing import List, Optional, TypeVar, Generic, Type
from datetime import datetime

class CarBase(BaseModel):
    model: str
    brand: str

class CarCreate(CarBase):
    pass

class Car(CarBase):
    id: int

    class Config:
        orm_mode = True

class CarUpdate(BaseModel):
    model: str
    brand: str

    class Config:
        orm_mode = True