import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db():
    conn = sqlite3.connect('storage.db')
    try:
        yield conn
    finally:
        conn.close()