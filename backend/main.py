from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/zbiorka_db")

@app.get("/api/zbiorki")
def get_zbiorki():
    # Połączenie backendu z bazą danych
    db_status = "Brak połączenia"
    try:
        conn = psycopg2.connect(DB_URL)
        db_status = "Pomyślnie połączono z PostgreSQL"
        conn.close()
    except Exception as e:
        db_status = f"Błąd bazy: {str(e)}"

    # Zwracanie danych w formacie JSON
    return {
        "status_bazy": db_status,
        "zbiorki": [
            {"id": 1, "cel": "Schronisko dla zwierząt", "zebrano": 1500},
            {"id": 2, "cel": "Odbudowa świetlicy", "zebrano": 5400}
        ]
    }