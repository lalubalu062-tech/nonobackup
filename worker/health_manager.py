import sqlite3
import time

DB="/home/jeet/nono/backend/nono.db"

MAX_RESTART=3


def check_health():

    print("Health Manager Started")


    while True:

        try:

            conn=sqlite3.connect(DB)
            cur=conn.cursor()


            cur.execute("""
            SELECT id,status,restart_count
            FROM projects
            WHERE status IN
            ('restarting','failed')
            """)


            rows=cur.fetchall()


            for project_id,status,count in rows:


                if count and count>=MAX_RESTART:

                    print(
                    "MARK FAILED",
                    project_id
                    )


                    cur.execute("""
                    UPDATE projects
                    SET status='failed',
                    health='dead',
                    last_error='Restart limit exceeded'
                    WHERE id=?
                    """,
                    (project_id,)
                    )



            conn.commit()
            conn.close()


        except Exception as e:

            print(
            "HEALTH ERROR",
            e
            )


        time.sleep(30)
