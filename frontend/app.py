from flask import Flask, render_template
import requests
import os
app = Flask(__name__, template_folder='.')
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

@app.route("/")
def index():
    try:
        response = requests.get(f"{BACKEND_URL}/api/zbiorki")
        data = response.json()
        if isinstance(data, list):
            data = {"status_bazy": "Połączono z backendem", "zbiorki": data}
        else:
            data = data
    except Exception as e:
        data = {"status_bazy": "Błąd połączenia z backendem", "zbiorki": [], "error": str(e)}

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)