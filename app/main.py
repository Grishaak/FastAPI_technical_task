from fastapi import FastAPI
from app.routers import table, reservation

app = FastAPI()

app.include_router(table.router, prefix="/tables", tags=["tables"])
app.include_router(reservation.router, prefix="/reservations", tags=["reservations"])

# Для теста
@app.get("/")
def read_root():
    return {"message": "Test_root"}
