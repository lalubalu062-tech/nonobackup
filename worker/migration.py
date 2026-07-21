import sqlite3
import time


DB="/home/jeet/nono/backend/nono.db"

OFFLINE_LIMIT=120


def find_worker(cur,old):

    cur.execute("""
    SELECT worker_id
    FROM workers
    WHERE status='online'
    AND worker_id!=?
    ORDER BY projects ASC
    LIMIT 1
    """,(old,))

    row=cur.fetchone()

    return row[0] if row else None



def migration():

    print("Migration Engine Started")


    while True:

        try:

            conn=sqlite3.connect(DB)
            cur=conn.cursor()


            now=time.time()


            # offline workers

            cur.execute("""
            SELECT worker_id,last_seen
            FROM workers
            WHERE status='offline'
            """)

            dead_workers=cur.fetchall()


            for worker,last in dead_workers:


                cur.execute("""
                SELECT id
                FROM projects
                WHERE worker_id=?
                AND status='running'
                """,
                (worker,))


                projects=cur.fetchall()


                for (pid,) in projects:


                    new=find_worker(
                        cur,
                        worker
                    )


                    if new:


                        print(
                        "MIGRATE",
                        pid,
                        worker,
                        "->",
                        new
                        )


                        cur.execute("""
                        UPDATE projects
                        SET
                        worker_id=?,
                        status='pending',
                        pid=NULL,
                        last_worker=?,
                        migration_count=
                        migration_count+1
                        WHERE id=?
                        """,
                        (
                        new,
                        worker,
                        pid
                        ))



            conn.commit()
            conn.close()


        except Exception as e:

            print(
            "MIGRATION ERROR",
            e
            )


        time.sleep(60)
