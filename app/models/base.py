from sqlmodel import SQLModel

class Base(SQLModel):
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
