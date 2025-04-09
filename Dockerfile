FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install alembic

COPY . .
COPY alembic.ini .
COPY alembic/ ./alembic/

# CMD ["uvicorn", "app.main:app","--host", "0.0.0.0", "--port", "8000"]
