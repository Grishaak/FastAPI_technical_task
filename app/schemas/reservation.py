from datetime import datetime

from pydantic import BaseModel


class ReservationCreate(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

class ReservationRead(ReservationCreate):
    id: int
