from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime, timedelta
from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.reservation import ReservationCreate, ReservationRead
from app.db.session import get_session
from sqlalchemy import func, and_, or_
from sqlalchemy.types import Interval 
router = APIRouter()

# GET /reservations/ - все брони
@router.get("/", response_model=list[ReservationRead])
def get_all_reservations(session: Session = Depends(get_session)):
    reservations = session.exec(select(Reservation)).all()
    return reservations

# POST /reservations/ - создать бронь (логика проверки конфликтов из предыдущего ответа)
@router.post("/", response_model=ReservationRead)
def create_reservation(
    reservation: ReservationCreate, 
    session: Session = Depends(get_session)
):
    # Проверка существования столика
    table = session.get(Table, reservation.table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Проверка конфликтов времени
    
    conflicting = check_reservation_conflict(session, reservation)


    if conflicting:
        raise HTTPException(
            status_code=400, 
            detail="Time slot already booked"
        )
    
    db_reservation = Reservation(**reservation.dict())
    session.add(db_reservation)
    session.commit()
    session.refresh(db_reservation)
    return db_reservation

# DELETE /reservations/{id} - удалить бронь
@router.delete("/{id}")
def delete_reservation(id: int, session: Session = Depends(get_session)):
    reservation = session.get(Reservation, id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    session.delete(reservation)
    session.commit()
    return {"message": "Reservation deleted"}

def check_reservation_conflict(session, reservation_data):
    new_start = reservation_data.reservation_time
    new_end = new_start + timedelta(minutes=reservation_data.duration_minutes)

    # Формируем условие для проверки пересечения временных интервалов
    conflict_condition = and_(
        Reservation.table_id == reservation_data.table_id,
        or_(
            and_(
                Reservation.reservation_time < new_end,
                func.timezone('UTC', Reservation.reservation_time) +
                (Reservation.duration_minutes * func.cast('1 minute', Interval)) > new_start
            ),
            and_(
                func.timezone('UTC', Reservation.reservation_time) < new_end,
                func.timezone('UTC', Reservation.reservation_time) +
                (Reservation.duration_minutes * func.cast('1 minute', Interval)) > new_start
            )
        )
    )

    return session.exec(
        select(Reservation).where(conflict_condition)
    ).first()
