import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db():
    conn = sqlite3.connect('storage.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MyTable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            emotion1 TEXT NOT NULL,
            emotion2 TEXT NOT NULL,
            emotion3 TEXT NOT NULL,
            response TEXT NOT NULL,
            createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    try:
        yield conn
    finally:
        conn.close()