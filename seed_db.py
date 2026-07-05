import sqlite3
from config import DB_PATH, SEED_SQL

def seed():
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SEED_SQL.read_text(encoding="utf-8"))
    conn.close()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for table in ["customers", "orders", "payments", "support_tickets"]:
        count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()
    print(f"Database seeded at {DB_PATH}")

if __name__ == "__main__":
    seed()
