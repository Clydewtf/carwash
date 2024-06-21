from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, index=True)
    brand = Column(String, index=True)

    customer_cars = relationship("CustomerCar", back_populates="car")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price_in_cents = Column(Integer)
    duration_in_seconds = Column(Integer)

    orders_assoc = relationship("OrderService", back_populates="service")
    orders = relationship("Order", secondary="order_services", back_populates="services")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role_id = Column(Integer)  # 1: Admin, 2: Employee, 3: Client
    is_send_notify = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    admin_orders = relationship("Order", foreign_keys="[Order.administrator_id]", back_populates="administrator")
    employee_orders = relationship("Order", foreign_keys="[Order.employee_id]", back_populates="employee")
    customer_cars = relationship("CustomerCar", back_populates="customer")


class CustomerCar(Base):
    __tablename__ = "customer_cars"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    number = Column(String, unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    car_id = Column(Integer, ForeignKey("cars.id"))

    customer = relationship("User", back_populates="customer_cars")
    car = relationship("Car", back_populates="customer_cars")
    orders = relationship("Order", back_populates="customer_car")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=0)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    total_time = Column(Integer)
    total_price = Column(Integer)
    administrator_id = Column(Integer, ForeignKey("users.id"))
    employee_id = Column(Integer, ForeignKey("users.id"))
    customer_car_id = Column(Integer, ForeignKey("customer_cars.id"))

    administrator = relationship("User", foreign_keys="[Order.administrator_id]", back_populates="admin_orders")
    employee = relationship("User", foreign_keys="[Order.employee_id]", back_populates="employee_orders")
    customer_car = relationship("CustomerCar", back_populates="orders")
    services_assoc = relationship("OrderService", back_populates="order")
    services = relationship("Service", secondary="order_services", back_populates="orders")


class OrderService(Base):
    __tablename__ = "order_services"

    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    service_id = Column(Integer, ForeignKey("services.id"), primary_key=True)

    order = relationship("Order", back_populates="services_assoc")
    service = relationship("Service", back_populates="orders_assoc")