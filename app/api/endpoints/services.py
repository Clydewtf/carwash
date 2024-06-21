from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from sqlalchemy import desc
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

@router.post("/", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_admin)):
    db_service = models.Service(
        name=service.name,
        price_in_cents=int(service.price_in_rubles * 100),  # рубли в копейки
        duration_in_seconds=service.duration_in_minutes * 60  # минуты в секунды
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.get("/", response_model=schemas.ResponseWrapper[schemas.ServiceVO])
def read_services(skip: int = 0, limit: int = 10, name: Optional[str] = None,
                  min_price: Optional[int] = None, max_price: Optional[int] = None,
                  sort_by: Optional[str] = None, sort_order: Optional[str] = "asc",
                  db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = db.query(models.Service)

    if name:
        query = query.filter(models.Service.name.ilike(f"%{name}%"))
    if min_price is not None:
        query = query.filter(models.Service.price_in_cents >= min_price * 100)
    if max_price is not None:
        query = query.filter(models.Service.price_in_cents <= max_price * 100)

    if sort_by:
        if sort_order == "desc":
            query = query.order_by(desc(getattr(models.Service, sort_by)))
        else:
            query = query.order_by(getattr(models.Service, sort_by))

    services = query.offset(skip).limit(limit).all()
    count = len(services)
    service_vos = []
    for service in services:
        price_vo = schemas.PriceVO(
            minValue=service.price_in_cents,
            maxValue=service.price_in_cents / 100,
            format=f"{service.price_in_cents / 100:.2f} руб."
        )
        time_vo = schemas.TimeVO(
            second=service.duration_in_seconds,
            minute=service.duration_in_seconds // 60
        )
        service_vo = schemas.ServiceVO(
            id=service.id,
            name=service.name,
            price=price_vo,
            time=time_vo
        )
        service_vos.append(service_vo)

    response = schemas.ResponseWrapper(
        data=service_vos,
        meta=schemas.Meta(count=count)
    )
    return response

@router.get("/{service_id}", response_model=schemas.ServiceVO)
def read_service(service_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")

    price_vo = schemas.PriceVO(
        minValue=db_service.price_in_cents,
        maxValue=db_service.price_in_cents // 100,
        format=f"{db_service.price_in_cents // 100} руб."
    )
    time_vo = schemas.TimeVO(
        second=db_service.duration_in_seconds,
        minute=db_service.duration_in_seconds // 60
    )
    service_vo = schemas.ServiceVO(
        id=db_service.id,
        name=db_service.name,
        price=price_vo,
        time=time_vo
    )
    return service_vo

@router.delete("/{service_id}", response_model=schemas.Service)
def delete_service(service_id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_admin)):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(db_service)
    db.commit()
    return db_service

@router.patch("/{service_id}", response_model=schemas.Service)
def update_service(service_id: int, service: schemas.ServiceUpdate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_admin)):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")

    if service.name:
        db_service.name = service.name
    if service.price_in_rubles is not None:
        db_service.price_in_cents = service.price_in_rubles * 100  # рубли в копейки
    if service.duration_in_minutes is not None:
        db_service.duration_in_seconds = service.duration_in_minutes * 60  # минуты в секунды

    db.commit()
    db.refresh(db_service)
    return db_service