CREATE TABLE airports (
    faa VARCHAR(10) PRIMARY KEY,  -- PK : code unique des aéroports
    name VARCHAR(100),
    lat DECIMAL(10, 6),
    lon DECIMAL(10, 6),
    alt INT,
    tz INT,
    dst CHAR(1),
    tzone VARCHAR(50)
);
CREATE TABLE airlines (
    carrier CHAR(2) PRIMARY KEY,  -- PK : code unique des compagnies aériennes
    name VARCHAR(100),
    faa_airport VARCHAR(10),
    FOREIGN KEY (faa_airport) REFERENCES airports(faa)  -- FK : fait référence à airports.faa
);
CREATE TABLE airline_airport_routes (
    carrier CHAR(2),  -- FK vers airlines.carrier
    faa VARCHAR(10),  -- FK vers airports.faa
    PRIMARY KEY (carrier, faa),
    FOREIGN KEY (carrier) REFERENCES airlines(carrier),
    FOREIGN KEY (faa) REFERENCES airports(faa)
);
CREATE TABLE planes (
    tailnum VARCHAR(10) PRIMARY KEY,  -- PK : numéro d'identification unique des avions
    year INT,
    type VARCHAR(50),
    manufacturer VARCHAR(100),
    model VARCHAR(50),
    engines INT,
    seats INT,
    speed INT,
    engine VARCHAR(50),
    carrier_airline CHAR(2),
    FOREIGN KEY (carrier_airline) REFERENCES airlines(carrier)  -- FK : référence vers airlines.carrier
);
CREATE TABLE flights (
    flight_id SERIAL PRIMARY KEY,  -- PK artificielle auto-incrémentée
    year INT,
    month INT,
    day INT,
    dep_time INT,
    sched_dep_time INT,
    dep_delay DECIMAL(5, 2),
    arr_time INT,
    sched_arr_time INT,
    arr_delay DECIMAL(5, 2),
    carrier CHAR(2),  -- FK vers airlines.carrier
    flight INT,
    tailnum VARCHAR(10),  -- FK vers planes.tailnum
    origin VARCHAR(10),  -- FK vers airports.faa (départ)
    dest VARCHAR(10),  -- FK vers airports.faa (arrivée)
    air_time DECIMAL(5, 2),
    distance DECIMAL(5, 2),
    hour INT,
    minute INT,
    time_hour TIMESTAMP,
    FOREIGN KEY (carrier) REFERENCES airlines(carrier),
    FOREIGN KEY (tailnum) REFERENCES planes(tailnum),
    FOREIGN KEY (origin) REFERENCES airports(faa),
    FOREIGN KEY (dest) REFERENCES airports(faa)
);
CREATE TABLE weather (
    year INT,
    month INT,
    day INT,
    hour INT,
    origin VARCHAR(10),  -- FK vers airports.faa
    temp DECIMAL(5, 2),
    dewp DECIMAL(5, 2),
    humid DECIMAL(5, 2),
    wind_dir INT,
    wind_speed DECIMAL(5, 2),
    wind_gust DECIMAL(5, 2),
    precip DECIMAL(5, 2),
    pressure DECIMAL(7, 2),
    visib DECIMAL(5, 2),
    time_hour TIMESTAMP,
    PRIMARY KEY (year, month, day, hour, origin),  -- PK composite
    FOREIGN KEY (origin) REFERENCES airports(faa)
);