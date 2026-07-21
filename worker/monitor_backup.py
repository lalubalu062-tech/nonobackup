import psutil
import time
import sqlite3

DB_PATH="/home/jeet/nono/backend/nono.db"

MAX_RAM_MB = 512
MAX_CPU_PERCENT = 80


def update_project(pid, reason="dead"):
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
                """
                UPDATE projects
                SET status='restarting',
                    pid=NULL
                WHERE id=?
                """,
                (row[0],)
            )

            conn.commit()

            print(
                "PROJECT RESTART QUEUED:",
                row[0],
                "REASON:",
                reason
            )

        conn.close()

    except Exception as e:
        print("MONITOR DB ERROR:",e)


def check_resource(pid):

    try:
        proc=psutil.Process(pid)

        ram = round(
            proc.memory_info().rss / 1024 / 1024,
            2
        )

        cpu = proc.cpu_percent(
            interval=1
        )

        if ram > MAX_RAM_MB:
            return False, f"RAM {ram}MB"

        if cpu > MAX_CPU_PERCENT:
            return False, f"CPU {cpu}%"

        return True, None

    except Exception as e:
        return False, str(e)


def monitor():

    print("NONO Project Monitor Started")

    while True:

        try:

            conn=sqlite3.connect(DB_PATH)
            cur=conn.cursor()

            cur.execute(
                """
                SELECT id,pid
                FROM projects
                WHERE status='running'
                AND pid IS NOT NULL
                """
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
                        "DEAD PID:",
                        project_id,
                        pid
                    )

                    update_project(
                        pid,
                        "dead"
                    )

                    continue



                ok,reason=check_resource(pid)


                if not ok:

                    print(
                        "RESOURCE LIMIT:",
                        project_id,
                        reason
                    )

                    update_project(
                        pid,
                        reason
                    )


        except Exception as e:

            print(
                "MONITOR ERROR:",
                e
            )


        time.sleep(30)
