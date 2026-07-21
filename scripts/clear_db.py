import sqlite3
import os
import glob

def clear_all_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "backend", "iki.db")
    uploads_dir = os.path.join(base_dir, "backend", "uploads")

    if os.path.exists(db_path):
        print(f"Opening database: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Tables found: {tables}")
        
        for table in tables:
            if table == "alembic_version":
                print("Preserving alembic_version table schema tracking.")
                continue
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"Table '{table}' had {count} rows. Deleting all rows...")
            cursor.execute(f"DELETE FROM {table}")
            
        conn.commit()
        conn.close()
        print("SQLite database cleared successfully.")
    else:
        print(f"No database file found at {db_path}.")

    if os.path.exists(uploads_dir):
        files = glob.glob(os.path.join(uploads_dir, "*"))
        removed_count = 0
        for f in files:
            if os.path.isfile(f):
                os.remove(f)
                removed_count += 1
        print(f"Cleared {removed_count} file(s) from uploads directory.")

if __name__ == "__main__":
    clear_all_data()
