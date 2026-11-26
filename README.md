# Projekt-MW
Projekt z metod wirtualizacji

Na pierwszy kamień milowy przygotowaliśmy pełen szkielet projektu oraz komunikacje między frontendem, backendem i db.

Użyliśmy AI do wygenerowania html strony frontendu oraz do elementów związanych z dodatkowymi bibliotekami w pythonie znajdujących się w plikach requirements.txt wraz z ich częściową implementacją.

## Dokumentacja API (Backend)

Format wymiany danych: **JSON**. Konfiguracja przez zmienne środowiskowe (`DATABASE_URL`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `BACKEND_URL`).

### Endpointy

1. **Status aplikacji**
   * `GET /health`
   * Odpowiedź (`200 OK`):
     ```json
     {
       "status": "ok"
     }
     ```

2. **Pobranie listy zbiórek**
   * `GET /api/zbiorki`
   * Odpowiedź (`200 OK`):
     ```json
     {
       "status_bazy": "Pomyślnie połączono z PostgreSQL",
       "zbiorki": [
         {
           "id": 1,
           "cel": "Schronisko dla zwierząt",
           "zebrano": 1500.0
         }
       ]
     }
     ```

3. **Pobranie pojedynczej zbiórki**
   * `GET /api/zbiorki/{zbiorka_id}`
   * Odpowiedź (`200 OK`):
     ```json
     {
       "id": 1,
       "cel": "Schronisko dla zwierząt",
       "zebrano": 1500.0
     }
     ```
   * Błąd (`404 Not Found`): gdy zbiórka o podanym ID nie istnieje.

4. **Dodanie nowej zbiórki**
   * `POST /api/zbiorki`
   * Ciało żądania (JSON):
     ```json
     {
       "cel": "Nowy sprzęt sportowy",
       "zebrano": 250.0
     }
     ```
   * Odpowiedź (`201 Created`): zwraca utworzony obiekt JSON z nadanym `id`.
   * Błąd (`400 Bad Request`): przy błędnych danych wejściowych (`cel` krótszy niż 3 znaki, brak wymaganego pola lub `zebrano < 0`).

5. **Aktualizacja istniejącej zbiórki**
   * `PUT /api/zbiorki/{zbiorka_id}`
   * Ciało żądania (JSON):
     ```json
     {
       "cel": "Schronisko dla zwierząt",
       "zebrano": 2000.0
     }
     ```
   * Odpowiedź (`200 OK`): zwraca zaktualizowany obiekt JSON.
   * Błędy: `400 Bad Request` (niepoprawne dane), `404 Not Found` (brak zasobu o podanym ID).
