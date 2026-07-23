import os
import json
import sqlite3
import psutil
import time

DB="/home/jeet/nono/backend/nono.db"
BASE="/home/jeet/nono/projects"
MAX_RESTART=5

def restart_loop():
    print("♻ Restart Manager Started")

    while True:
        try:
            conn=sqlite3.connect(DB)
            cur=conn.cursor()

            cur.execute("""
            SELECT id,pid,restart_count,status
            FROM projects
            WHERE status='running'
            """)

            rows=cur.fetchall()

            for project_id,pid,restarts,status in rows:

                if not pid:
                    continue

                if psutil.pid_exists(pid):
                    continue

                print("PROCESS DEAD",project_id)

                if restarts>=MAX_RESTART:

                    cur.execute("""
                    UPDATE projects
                    SET status='failed',
                        last_error='Restart limit exceeded'
                    WHERE id=?
                    """,(project_id,))

                    continue

                cur.execute("""
                UPDATE projects
                SET status='pending',
                    pid=NULL,
                    restart_count=restart_count+1
                WHERE id=?
                """,(project_id,))

                pidfile=f"{BASE}/{project_id}/pid.json"

                if os.path.exists(pidfile):
                    os.remove(pidfile)

                print("RESTART QUEUED",project_id)

            conn.commit()
            conn.close()

        except Exception as e:
            print("RESTART ERROR",e)

        time.sleep(10)
