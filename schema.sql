CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE boardgames (
    id INTEGER PRIMARY KEY,
    boardgame_name TEXT,
    duration TEXT,
    players_min TEXT,
    players_max TEXT,
    age_limit TEXT,
    genre TEXT,
    user_id INTEGER REFERENCES users
);