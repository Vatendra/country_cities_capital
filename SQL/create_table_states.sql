CREATE TABLE IF NOT EXISTS cities_db.states (
    id INTEGER PRIMARY KEY,
    country_id INTEGER REFERENCES cities_db.countries(id),
    state_name VARCHAR(64) NOT NULL,
    state_code VARCHAR(8) NOT NULL,
    latitude VARCHAR(16) NOT NULL,
    longitude VARCHAR(16) NOT NULL
);