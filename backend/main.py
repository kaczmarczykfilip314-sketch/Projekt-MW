from fastapi import FastAPI, HTTPException, status
import psycopg2
import os
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Platforma Zbiórek API")

DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/zbiorka_db")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Błędne dane wejściowe", "errors": exc.errors()},
    )


class ZbiorkaIn(BaseModel):
    cel: str = Field(..., min_length=3, max_length=255)
    zebrano: float = Field(default=0, ge=0)

@app.get("/api/zbiorki")
def get_zbiorki():
    db_status = "Brak połączenia"
    zbiorki = []
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, cel, zebrano FROM zbiorki ORDER BY id;")
        rows = cur.fetchall()
        zbiorki = [{"id": r[0], "cel": r[1], "zebrano": float(r[2])} for r in rows]
        cur.close()
        conn.close()
    except Exception as e:
        db_status = f"Błąd bazy: {str(e)}"
    return {
        "status_bazy": db_status,
        "zbiorki": zbiorki
    }

@app.get("/health")
def health():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Błąd połączenia z bazą: {str(e)}",
        )
        
@app.get("/api/zbiorki/{zbiorka_id}")
def get_zbiorka(zbiorka_id: int):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, cel, zebrano FROM zbiorki WHERE id = %s;", (zbiorka_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zbiórka nie została znaleziona")
    return {"id": row[0], "cel": row[1], "zebrano": float(row[2])}
