import psycopg2
import sys

db_url = "postgresql://postgres:DrsIkVDLGkYAmzoWyVCQgVlyZOKXneoy@centerbeam.proxy.rlwy.net:36554/railway?sslmode=require"

try:
    print("Connecting to DB...")
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT pid, state, query FROM pg_stat_activity WHERE state != 'idle';")
    rows = cur.fetchall()
    print(f"Active DB connections: {len(rows)}")
    for r in rows:
        print(r)
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
