import psycopg2
import sys

db_url = "postgresql://postgres:DrsIkVDLGkYAmzoWyVCQgVlyZOKXneoy@centerbeam.proxy.rlwy.net:36554/railway?sslmode=require"

try:
    print("Connecting to DB...")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cur.fetchall()
    print("Tables in DB:")
    for t in tables:
        print(t[0])
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
