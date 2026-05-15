from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = BASE_DIR / "accounting.db"


class DatabaseManager:
    def __init__(self):
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                note TEXT
            )
        """)

        cursor.execute("PRAGMA table_info(records)")
        columns = cursor.fetchall()

        column_names = []
        for column in columns:
            column_names.append(column[1])

        if "date" not in column_names:
            cursor.execute("ALTER TABLE records ADD COLUMN date TEXT")

        cursor.execute(
            "UPDATE records SET date = ? WHERE date IS NULL",
            ("未知日期",)
        )

        conn.commit()
        conn.close()

    def execute_sql(self, sql, params=()):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(sql, params)

        conn.commit()
        conn.close()

    def fetch_all(self, sql, params=()):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(sql, params)
        results = cursor.fetchall()

        conn.close()

        return results

    def fetch_one(self, sql, params=()):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(sql, params)
        result = cursor.fetchone()

        conn.close()

        return result