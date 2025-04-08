from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..models.table import Table
from ..schemas.table import TableCreate, TableRead
from ..db.session import get_session

router = APIRouter()


@router.post("/tables", response_model=TableRead)
def create_table(table: TableCreate, session: Session = Depends(get_session)):
    db_table = Table(**table.dict())
    session.add(db_table)
    session.commit()
    session.refresh(db_table)
    return db_table


# Аналогично GET и DELETE
@router.delete("/tables/id:<int>", response_model=TableRead)
def delete_table(table: TableCreate, session: Session = Depends(get_session)):
    db_table = Table(**table.dict())
    session.add(db_table)
    session.commit()
    session.refresh(db_table)
    return db_table


@router.get("/tables", response_model=TableRead)
def get_tables(table: TableCreate, session: Session = Depends(get_session)):
    db_table = Table(**table.dict())
    session.add(db_table)
    session.commit()
    session.refresh(db_table)
    return db_table


