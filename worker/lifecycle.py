import sqlite3
import time
import psutil


DB="/home/jeet/nono/backend/nono.db"

SLEEP_TIME=900


def lifecycle():

    print("Lifecycle Manager Started")


    while True:

        try:

            conn=sqlite3.connect(DB)

            cur=conn.cursor()


            cur.execute("""
            SELECT id,pid,last_activity,status
            FROM projects
            WHERE status='running'
            """)


            rows=cur.fetchall()


            now=time.time()


            for pid_data in rows:

                project_id,pid,last,status=pid_data


                if not last:
                    continue


                if now-last>SLEEP_TIME:

                    print(
                    "SLEEP PROJECT",
                    project_id
                    )


                    if pid and psutil.pid_exists(pid):

                        psutil.Process(pid).kill()


                    cur.execute("""
                    UPDATE projects
                    SET status='sleeping',
                    pid=NULL
                    WHERE id=?
                    """,
                    (project_id,)
                    )


            conn.commit()
            conn.close()


        except Exception as e:

            print(
            "LIFECYCLE ERROR",
            e
            )


        time.sleep(60)
