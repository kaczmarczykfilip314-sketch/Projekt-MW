from flask import Flask, render_template_string
import requests
import os

app = Flask(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

@app.route("/")
def index():
    try:
        response = requests.get(f"{BACKEND_URL}/api/zbiorki")
        data = response.json()
    except Exception as e:
        data = {"status_bazy": "Błąd połączenia z backendem", "zbiorki": [], "error": str(e)}

    html = """
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>Platforma Zbiórek Pieniędzy</title>
        <style>body { font-family: Arial, sans-serif; padding: 20px; }</style>
    </head>
    <body>
        <h1>Platforma Zbiórek Pieniędzy</h1>
        <p><strong>Status bazy danych (info z backendu):</strong> {{ data.status_bazy }}</p>
        
        <h2>Aktywne zbiórki:</h2>
        <ul>
        {% for zbiorka in data.zbiorki %}
            <li><strong>Cel:</strong> {{ zbiorka.cel }} | <strong>Zebrano:</strong> {{ zbiorka.zebrano }} PLN</li>
        {% else %}
            <li>Brak danych do wyświetlenia.</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html, data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)