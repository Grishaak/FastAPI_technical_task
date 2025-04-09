from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .table import Table

class Reservation(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_name: str
    table_id: Optional[int] = Field(foreign_key="table.id")
    reservation_time: datetime
    duration_minutes: int
    table: Optional["Table"] = Relationship(back_populates="reservations")
