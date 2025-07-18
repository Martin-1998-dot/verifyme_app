#!/bin/bash
echo "🔐 Creating admin table and adding default admin user..."

# Create admin table if not exists
sqlite3 verifyme.sqlite <<SQL
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
SQL

# Hash password using PHP CLI
HASHED_PASS=$(php -r "echo password_hash('admin123', PASSWORD_DEFAULT);")

# Insert default admin if not exists
sqlite3 verifyme.sqlite <<SQL
INSERT OR IGNORE INTO admin (username, password) VALUES ('admin', '$HASHED_PASS');
SQL

echo "✅ Admin user created: username='admin', password='admin123'"
