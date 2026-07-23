import sqlite3
import time
import psutil

DB="/home/jeet/nono/backend/nono.db"

def restart_loop():
    print("🔄 Restart Queue Started")

    while True:
        try:
            conn=sqlite3.connect(DB)
            cur=conn.cursor()

            cur.execute("""
            SELECT id,pid
            FROM projects
            WHERE status='restarting'
            """)

            rows=cur.fetchall()

            for pid_data in rows:
                project_id,pid=pid_data

                if pid and psutil.pid_exists(pid):
                    continue

                cur.execute("""
                UPDATE projects
                SET status='pending',
                    pid=NULL
                WHERE id=?
                """,(project_id,))

                conn.commit()

                print("♻️ Restart queued:",project_id)

            conn.close()

        except Exception as e:
            print("Restart Queue:",e)

        time.sleep(5)
