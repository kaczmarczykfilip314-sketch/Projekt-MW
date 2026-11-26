from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/zbiorka_db")

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
        db_status = "Pomyślnie połączono z PostgreSQL"
        conn.close()
    except Exception as e:
        db_status = f"Błąd bazy: {str(e)}"
    return {
        "status_bazy": db_status,
        "zbiorki": zbiorki
    }


@app.get("/health")
def health():
    return {"status": "ok"}



















