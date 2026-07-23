import sqlite3
import psutil
import time

DB="/home/jeet/nono/backend/nono.db"

def status_sync():
    print("🔄 Status Sync Started")

    while True:
        try:
            conn=sqlite3.connect(DB)
            cur=conn.cursor()

            cur.execute("""
            SELECT id,pid,status
            FROM projects
            """)

            rows=cur.fetchall()

            for project_id,pid,status in rows:

                if status=="running":
                    if not pid or not psutil.pid_exists(pid):
                        cur.execute("""
                        UPDATE projects
                        SET status='restarting',
                            pid=NULL
                        WHERE id=?
                        """,(project_id,))

                elif status=="stopped":
                    cur.execute("""
                    UPDATE projects
                    SET pid=NULL
                    WHERE id=?
                    """,(project_id,))

            conn.commit()
            conn.close()

        except Exception as e:
            print("STATUS SYNC:",e)

        time.sleep(5)
