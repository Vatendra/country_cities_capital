CREATE TABLE IF NOT EXISTS cities_db.cities (
    id INTEGER PRIMARY KEY,
    city_name VARCHAR(64) NOT NULL,
    country_id INTEGER REFERENCES cities_db.countries(id),
    state_id INTEGER REFERENCES cities_db.states(id),
    latitude VARCHAR(16) NOT NULL,
    longitude VARCHAR(16) NOT NULL
);