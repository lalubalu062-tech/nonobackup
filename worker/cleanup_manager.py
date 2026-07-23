import os
import time
import json
import sqlite3
import psutil
import shutil

DB="/home/jeet/nono/backend/nono.db"
PROJECTS="/home/jeet/nono/projects"


def clean():

    print("🧹 Auto Cleanup Started")

    while True:
        try:
            conn=sqlite3.connect(DB)
            cur=conn.cursor()

            cur.execute("""
            SELECT id,status,pid
            FROM projects
            """)

            rows=cur.fetchall()

            for project_id,status,pid in rows:

                # dead pid cleanup
                if pid:

                    if not psutil.pid_exists(pid):

                        print(
                            "ORPHAN PID CLEAN",
                            project_id,
                            pid
                        )

                        cur.execute("""
                        UPDATE projects
                        SET pid=NULL,
                        status='stopped'
                        WHERE id=?
                        """,(project_id,))


                # remove old pid.json
                pidfile=f"{PROJECTS}/{project_id}/pid.json"

                if os.path.exists(pidfile):

                    try:
                        with open(pidfile) as f:
                            data=json.load(f)

                        if data.get("pid") and not psutil.pid_exists(
                            data["pid"]
                        ):
                            os.remove(pidfile)
                            print(
                                "PID FILE REMOVED",
                                project_id
                            )

                    except:
                        pass


                # cleanup failed folders
                if status in (
                    "failed",
                    "stopped"
                ):

                    appdir=f"{PROJECTS}/{project_id}/app"

                    if os.path.exists(appdir):

                        # keep latest app for stopped
                        pass


            conn.commit()
            conn.close()

        except Exception as e:
            print(
                "CLEANUP ERROR",
                e
            )

        time.sleep(60)


if __name__=="__main__":
    clean()
