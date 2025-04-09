from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .reservation import Reservation

class Table(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    seats: int
    location: str
    reservations: List["Reservation"] = Relationship(back_populates="table")
