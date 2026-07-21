import sqlite3
import time


DB="/home/jeet/nono/backend/nono.db"


OFFLINE_TIME=120


def scheduler():

    print("Scheduler Started")


    while True:

        try:

            conn=sqlite3.connect(DB)
            cur=conn.cursor()


            now=time.time()


            cur.execute(
            """
            SELECT worker_id,last_seen
            FROM workers
            """
            )


            workers=cur.fetchall()


            for wid,last in workers:

                if last and now-last>OFFLINE_TIME:

                    print(
                    "WORKER OFFLINE",
                    wid
                    )


                    cur.execute(
                    """
                    UPDATE workers
                    SET status='offline'
                    WHERE worker_id=?
                    """,
                    (wid,)
                    )


            conn.commit()
            conn.close()


        except Exception as e:

            print(
            "SCHEDULER ERROR",
            e
            )


        time.sleep(60)
