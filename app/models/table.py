from sqlmodel import SQLModel, Field


class Table(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    seats: int
    location: str
