import psutil
import time
import sqlite3
import os
import json


DB_PATH="/home/jeet/nono/backend/nono.db"

MAX_RAM_MB=512
MAX_CPU_PERCENT=80

IDLE_LIMIT=900   # 15 minutes


def kill_process(pid):

    try:

        p=psutil.Process(pid)

        for child in p.children(
            recursive=True
        ):

            child.kill()


        p.kill()

        return True


    except Exception as e:

        print(
            "KILL ERROR",
            e
        )

        return False



def queue_restart(pid):

    try:

        conn=sqlite3.connect(DB_PATH)

        cur=conn.cursor()


        cur.execute(
        """
        SELECT id 
        FROM projects 
        WHERE pid=?
        """,
        (pid,)
        )


        row=cur.fetchone()


        if row:

            cur.execute(
            """
            UPDATE projects
            SET status='restarting',
            pid=NULL,
            restart_count=restart_count+1
            WHERE id=?
            """,
            (row[0],)
            )

            conn.commit()

            print(
                "RESTART QUEUED",
                row[0]
            )


        conn.close()


    except Exception as e:

        print(
            "DB ERROR",
            e
        )



def monitor():

    print(
        "Resource Isolation Started"
    )


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


                if not psutil.pid_exists(pid):

                    continue



                try:


                    p=psutil.Process(pid)


                    ram=round(
                    p.memory_info().rss/1024/1024,
                    2
                    )


                    cpu=p.cpu_percent(
                        interval=1
                    )



                    print(
                    "CHECK",
                    project_id,
                    "RAM",
                    ram,
                    "CPU",
                    cpu
                    )



                    if ram > MAX_RAM_MB:


                        print(
                        "RAM LIMIT",
                        project_id
                        )


                        kill_process(pid)

                        queue_restart(pid)



                    elif cpu > MAX_CPU_PERCENT:


                        print(
                        "CPU LIMIT",
                        project_id
                        )


                        kill_process(pid)

                        queue_restart(pid)



                except psutil.NoSuchProcess:

                    pass



        except Exception as e:

            print(
            "MONITOR ERROR",
            e
            )


        time.sleep(30)
