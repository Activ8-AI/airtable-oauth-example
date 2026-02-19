import sqlite3
import os
import datetime

DB_PATH = "custody/custodian_ledger.db"
_SCHEMA_INITIALIZED = False

def connect():
    return sqlite3.connect(DB_PATH)

def write_record(event_type, payload):
    conn = connect()
    cursor = conn.cursor()
    global _SCHEMA_INITIALIZED
    if not _SCHEMA_INITIALIZED:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ledger(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event_type TEXT,
                payload TEXT
            )
        """)
        _SCHEMA_INITIALIZED = True

    cursor.execute(
        "INSERT INTO ledger (timestamp, event_type, payload) VALUES (?, ?, ?)",
        (datetime.datetime.now().isoformat(), event_type, str(payload)),
    )
    conn.commit()
    conn.close()
