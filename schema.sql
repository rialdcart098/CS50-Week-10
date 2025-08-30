CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    birth DATE,
    age INTEGER,
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

--CREATE TABLE academics (
--
--    user_id INTEGER PRIMARY KEY AUTOINCREMENT
--    grade INTEGER NOT NULL,
--
--);




--Dropping databases after testing

-- DROP TABLE users;
-- DROP TABLE academics;