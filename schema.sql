CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    birth DATE,
    age INTEGER,
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL
);

CREATE TABLE units (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    unit TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);

CREATE TABLE tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    test TEXT NOT NULL,
    score INTEGER,
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subject_id TEXT NOT NULL,
    subject_name TEXT NOT NULL,
    question_amount INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (subject_name) REFERENCES subjects(subject),
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);
CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    unit_id INTEGER NOT NULL,
    questionsDone INTEGER NOT NULL,
    questionsCorrect INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (unit_id) REFERENCES units(id)
);

INSERT INTO subjects (subject) VALUES ('algebra1');
INSERT INTO subjects (subject) VALUES ('geometry');
INSERT INTO subjects (subject) VALUES ('algebra2');

INSERT INTO units (subject_id, unit) VALUES
    (1, 'Number & Quantity'),
    (1, 'Algebra'),
    (1, 'Functions'),
    (1, 'Statistics & Probability');

INSERT INTO units (subject_id, unit) VALUES
    (2, 'Congruence'),
    (2, 'Similarity'),
    (2, 'Right Triangles & Trigonometry'),
    (2, 'Circles'),
    (2, 'Expressing Geometric Properties with Equations'),
    (2, 'Geometric Measurement & Dimension'),
    (2, 'Modeling with Geometry');

INSERT INTO units (subject_id, unit) VALUES
    (3, 'Polynomial Functions'),
    (3, 'Rational Functions'),
    (3, 'Exponential & Logarithmic Functions'),
    (3, 'Trigonometric Functions');



