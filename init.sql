CREATE TABLE IF NOT EXISTS zbiorki (
    id SERIAL PRIMARY KEY,
    cel TEXT NOT NULL,
    zebrano NUMERIC NOT NULL
);

COPY zbiorki (cel, zebrano)
FROM '/zbiorki.txt'
WITH (FORMAT csv, DELIMITER ';');