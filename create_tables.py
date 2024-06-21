from app.database import Base, engine
from app.models import Car, Service, User, CustomerCar, Order, OrderService

# Создание всех таблиц
Base.metadata.create_all(bind=engine)