from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.table import Table
from app.schemas.table import TableCreate, TableRead
from app.db.session import get_session

router = APIRouter()


@router.get("/", response_model=list[TableRead])
def get_all_tables(session: Session = Depends(get_session)):
    tables = session.exec(select(Table)).all()
    return tables

# POST /tables/ - создать столик
@router.post("/", response_model=TableRead)
def create_table(table: TableCreate, session: Session = Depends(get_session)):
    db_table = Table(**table.dict())
    session.add(db_table)
    session.commit()
    session.refresh(db_table)
    return db_table

# DELETE /tables/{id} - удалить столик
@router.delete("/{id}")
def delete_table(id: int, session: Session = Depends(get_session)):
    table = session.get(Table, id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    session.delete(table)
    session.commit()
    return {"message": "Table deleted"}
