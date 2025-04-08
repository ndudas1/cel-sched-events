CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    frequency INT DEFAULT NULL
);

Insert INTO events (name, email, notes, start_time, end_time, frequency)
 Values ('nick', 'email', 'no notes', '2025-10-01T22:00:00-07:00', '2025-10-01T23:00:00-07:00', 2);