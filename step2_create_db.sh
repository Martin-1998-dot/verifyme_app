#!/bin/bash
echo "🗄️ Creating SQLite database and users table..."
sqlite3 verifyme.sqlite <<SQL
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    id_image TEXT,
    status TEXT DEFAULT 'Pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SQL
echo "✅ Database and users table ready."
