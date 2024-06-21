from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Path
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app import crud, models, schemas
from app.database import SessionLocal
from datetime import datetime, timedelta
from app.dependencies import get_current_user, get_current_admin
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def send_email_notification(email: str, subject: str, message: str):
    smtp_server = "smtp.mail.ru"
    smtp_port = 465
    smtp_user = "legitskull@mail.ru"
    smtp_password = "c4bupijjbqezmFr66QRW"
    # smtp_password = "Psf-NLe-tY7-vrW"
    # smtp_user = "clydegenshin@mail.ru"
    # smtp_password = "MI6YOppeby2"

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        # server = smtplib.SMTP(smtp_server, smtp_port)
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        # server.starttls()
        server.login(smtp_user, smtp_password)
        # server.sendmail(smtp_user, email, msg.as_string())
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Error sending email: {e}")


    print(f"Sending email to {email}: {subject} - {message}")

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db),
                 current_user: models.User = Depends(get_current_admin)):
    total_price = 0
    total_time = 0
    services = []
    for service_id in order.service_ids:
        service = db.query(models.Service).filter(models.Service.id == service_id).first()
        if service:
            total_price += service.price_in_cents
            total_time += service.duration_in_seconds
            services.append(service)

    end_date = datetime.utcnow() + timedelta(seconds=total_time)

    db_order = models.Order(
        customer_car_id=order.customer_car_id,
        employee_id=order.employee_id,
        start_date=datetime.utcnow(),
        end_date=end_date,
        total_time=total_time,
        total_price=total_price,
        administrator_id=current_user.id,
        status=order.status
    )
    db_order.services = services
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/{order_id}", response_model=schemas.OrderDetail)
def read_order(order_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user.role_id == 2 and db_order.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if current_user.role_id == 3 and db_order.customer_car.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    order_detail = schemas.OrderDetail(
        id=db_order.id,
        status=db_order.status,
        start_date=db_order.start_date,
        end_date=db_order.end_date,
        total_time=db_order.total_time // 60,  # в минутах
        total_price=db_order.total_price // 100,  # в рублях
        administrator={
            "id": db_order.administrator.id,
            "fullName": db_order.administrator.full_name
        },
        employee={
            "id": db_order.employee.id,
            "fullName": db_order.employee.full_name
        },
        customer_car={
            "id": db_order.customer_car.id,
            "year": db_order.customer_car.year,
            "number": db_order.customer_car.number,
            "customer": {
                "id": db_order.customer_car.customer.id,
                "fullName": db_order.customer_car.customer.full_name,
                "email": db_order.customer_car.customer.email
            },
            "car": {
                "model": db_order.customer_car.car.model,
                "brand": db_order.customer_car.car.brand
            }
        }
    )
    return order_detail

@router.get("/", response_model=schemas.ResponseWrapper[schemas.OrderDetail])
def read_orders(skip: int = 0, limit: int = 10, status: Optional[int] = None,
                customer_car_id: Optional[int] = None, employee_id: Optional[int] = None,
                sort_by: Optional[str] = None, sort_order: Optional[str] = "asc",
                db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = db.query(models.Order)

    if current_user.role_id == 1:  # админ
        if status is not None:
            query = query.filter(models.Order.status == status)
        if customer_car_id is not None:
            query = query.filter(models.Order.customer_car_id == customer_car_id)
        if employee_id is not None:
            query = query.filter(models.Order.employee_id == employee_id)
    elif current_user.role_id == 2:  # работник
        query = query.filter(models.Order.employee_id == current_user.id)
        if status is not None:
            query = query.filter(models.Order.status == status)
    elif current_user.role_id == 3:  # клиент
        query = query.join(models.CustomerCar).filter(models.CustomerCar.customer_id == current_user.id)
        if status is not None:
            query = query.filter(models.Order.status == status)
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if sort_by:
        if sort_order == "desc":
            query = query.order_by(desc(getattr(models.Order, sort_by)))
        else:
            query = query.order_by(getattr(models.Order, sort_by))

    orders = query.offset(skip).limit(limit).all()
    count = len(orders)
    order_details = []
    for db_order in orders:
        order_detail = schemas.OrderDetail(
            id=db_order.id,
            status=db_order.status,
            start_date=db_order.start_date,
            end_date=db_order.end_date,
            total_time=db_order.total_time // 60,  # в минутах
            total_price=db_order.total_price // 100,  # в рублях
            administrator={
                "id": db_order.administrator.id,
                "fullName": db_order.administrator.full_name
            },
            employee={
                "id": db_order.employee.id,
                "fullName": db_order.employee.full_name
            },
            customer_car={
                "id": db_order.customer_car.id,
                "year": db_order.customer_car.year,
                "number": db_order.customer_car.number,
                "customer": {
                    "id": db_order.customer_car.customer.id,
                    "fullName": db_order.customer_car.customer.full_name,
                    "email": db_order.customer_car.customer.email
                },
                "car": {
                    "model": db_order.customer_car.car.model,
                    "brand": db_order.customer_car.car.brand
                }
            }
        )
        order_details.append(order_detail)

    response = schemas.ResponseWrapper(
        data=order_details,
        meta=schemas.Meta(count=count)
    )

    return response

@router.patch("/{order_id}/status", response_model=schemas.Order)
def update_order_status(order_id: int, order_update: schemas.OrderUpdateStatus,
                        db: Session = Depends(get_db),
                        current_user: models.User = Depends(get_current_admin),
                        background_tasks: BackgroundTasks = BackgroundTasks()):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db_order.status = order_update.status
    db.commit()
    db.refresh(db_order)

    if db_order.status == 2:
        customer = db.query(models.User).join(models.CustomerCar).filter(
            models.CustomerCar.id == db_order.customer_car_id).first()
        if customer and customer.is_send_notify:
            print("rabotaet")
            subject = "Ваш заказ выполнен"
            message = f"Уважаемый {customer.full_name}, ваш заказ выполнен."
            background_tasks.add_task(send_email_notification, customer.email, subject, message)

    return db_order

@router.delete("/{order_id}", response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return db_order


@router.post("/{order_id}/add_services", response_model=schemas.Order)
def add_services_to_order(order_id: int, services: List[int], db: Session = Depends(get_db),
                          current_user: models.User = Depends(get_current_admin)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if db_order.status != 1:
        raise HTTPException(status_code=400, detail="Cannot add services to a completed order")

    existing_service_ids = {service.id for service in db_order.services}
    for service_id in services:
        if service_id in existing_service_ids:
            service = db.query(models.Service).filter(models.Service.id == service_id).first()
            raise HTTPException(status_code=400, detail=f"Service '{service.name}' is already in the order")

    total_price = db_order.total_price
    total_time = db_order.total_time
    for service_id in services:
        service = db.query(models.Service).filter(models.Service.id == service_id).first()
        if service:
            db_order.services.append(service)
            total_price += service.price_in_cents
            total_time += service.duration_in_seconds

    db_order.total_price = total_price
    db_order.total_time = total_time
    db_order.end_date = db_order.start_date + timedelta(seconds=total_time)

    db.commit()
    db.refresh(db_order)
    return db_order