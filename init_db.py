"""Seed script — run once to create bank.db for local testing of main.py."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bank.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id TEXT PRIMARY KEY,
    owner TEXT NOT NULL,
    balance REAL NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
""")

cur.execute("INSERT OR IGNORE INTO accounts VALUES ('acct-001', 'alice', 5000.00)")
cur.execute("INSERT OR IGNORE INTO accounts VALUES ('acct-002', 'bob', 12000.00)")

conn.commit()
conn.close()
print(f"Seeded {DB_PATH}")
