from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime, timedelta

from models.table import Table
from models.reservation import Reservation
from schemas.reservation import ReservationCreate, ReservationRead
from db.session import get_session

router = APIRouter()


def check_reservation_conflict(session, reservation_data):
    new_end = reservation_data.reservation_time + timedelta(
        minutes=reservation_data.duration_minutes
    )

    conflicting = session.exec(
        select(Reservation).where(
            Reservation.table_id == reservation_data.table_id,
            Reservation.reservation_time < new_end,
            Reservation.reservation_time + (
                    Reservation.duration_minutes * 60 * 1000000
            ) > int(reservation_data.reservation_time.timestamp() * 1000000)
        )
    ).first()
    return conflicting


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
    if check_reservation_conflict(session, reservation):
        raise HTTPException(
            status_code=400,
            detail="Time slot already booked"
        )

    db_reservation = Reservation(**reservation.dict())
    session.add(db_reservation)
    session.commit()
    session.refresh(db_reservation)
    return db_reservation
