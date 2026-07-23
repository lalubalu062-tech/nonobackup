import os
import signal
import sqlite3
import time

DB="/home/jeet/nono/backend/nono.db"

def shutdown_all():
    print("🛑 Shutdown Manager Started")

    try:
        conn=sqlite3.connect(DB)
        cur=conn.cursor()

        cur.execute("""
        SELECT id,pid
        FROM projects
        WHERE status='running'
        AND pid IS NOT NULL
        """)

        rows=cur.fetchall()

        for project_id,pid in rows:
            try:
                print("STOP PROJECT",project_id,pid)

                os.kill(pid,signal.SIGTERM)

                time.sleep(2)

                cur.execute("""
                UPDATE projects
                SET status='stopped',
                pid=NULL
                WHERE id=?
                """,(project_id,))

                print("STOPPED",project_id)

            except Exception as e:
                print("STOP ERROR",project_id,e)

        conn.commit()
        conn.close()

    except Exception as e:
        print("SHUTDOWN ERROR",e)

if __name__=="__main__":
    shutdown_all()
