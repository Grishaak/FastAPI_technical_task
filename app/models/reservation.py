from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

from app.models.table import Table


class Reservation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_name: str
    table_id: int = Field(foreign_key="table.id")
    reservation_time: datetime
    duration_minutes: int
    table: Table = Relationship(back_populates="reservations")
