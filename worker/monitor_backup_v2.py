import psutil
import time
import sqlite3

DB_PATH="/home/jeet/nono/backend/nono.db"

def update_project(pid):
    try:
        conn=sqlite3.connect(DB_PATH)
        cur=conn.cursor()

        cur.execute(
            "SELECT id FROM projects WHERE pid=?",
            (pid,)
        )

        row=cur.fetchone()

        if row:
            cur.execute(
                "UPDATE projects SET status='restarting', pid=NULL WHERE id=?",
                (row[0],)
            )
            conn.commit()
            print("PROJECT RESTART QUEUED:", row[0])

        conn.close()

    except Exception as e:
        print("MONITOR DB ERROR:",e)


def monitor():
    print("NONO Project Monitor Started")

    while True:
        try:
            conn=sqlite3.connect(DB_PATH)
            cur=conn.cursor()

            cur.execute(
                "SELECT id,pid FROM projects WHERE status='running' AND pid IS NOT NULL"
            )

            projects=cur.fetchall()
            conn.close()

            for project_id,pid in projects:
                dead=False

                if not psutil.pid_exists(pid):
                    dead=True
                else:
                    try:
                        proc=psutil.Process(pid)
                        if proc.status()==psutil.STATUS_ZOMBIE:
                            dead=True
                    except psutil.NoSuchProcess:
                        dead=True

                if dead:
                    print(
                        "DEAD/ZOMBIE PID:",
                        project_id,
                        pid
                    )
                    update_project(pid)

        except Exception as e:
            print("MONITOR ERROR:",e)

        time.sleep(30)
