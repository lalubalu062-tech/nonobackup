import os
import json
import time
import psutil
import signal
import sqlite3
from datetime import datetime

FILE="processes.json"
MAX_RAM_MB=512
MAX_CPU_PERCENT=50
DB_PATH="/home/jeet/nono/backend/nono.db"


def save(data):
    with open(FILE,"w") as f:
        json.dump(data,f,indent=2)


def db_update(project_id,status):
    try:
        conn=sqlite3.connect(DB_PATH)
        cur=conn.cursor()

        cur.execute(
            "UPDATE projects SET status=? WHERE id=?",
            (status,project_id)
        )

        conn.commit()
        conn.close()

        print(
            "DB:",
            project_id,
            status
        )

    except Exception as e:
        print("DB ERROR:",e)


def kill_project(project_id,pid,data):
    try:
        os.kill(pid,signal.SIGTERM)

    except:
        pass

    data[str(project_id)]["status"]="killed"
    db_update(project_id,"killed")

    print(
        "Killed:",
        project_id
    )


def check():

    if not os.path.exists(FILE):
        return

    with open(FILE) as f:
        data=json.load(f)


    changed=False


    for project,item in data.items():

        if item.get("status")!="running":
            continue


        pid=item.get("pid")


        if not pid:
            continue


        try:

            proc=psutil.Process(pid)


            if not proc.is_running() or proc.status() == psutil.STATUS_ZOMBIE:

                item["status"]="restarting"
                db_update(project,"stopped")
                changed=True
                continue


            ram=proc.memory_info().rss/1024/1024
            cpu=proc.cpu_percent(interval=1)


            item["ram_mb"]=round(ram,2)
            item["cpu_percent"]=cpu
            item["checked"]=str(datetime.utcnow())


            print(
                f"PROJECT {project} RAM {ram:.2f}MB CPU {cpu}%"
            )


            if ram > MAX_RAM_MB or cpu > MAX_CPU_PERCENT:

                kill_project(
                    project,
                    pid,
                    data
                )

                changed=True


        except psutil.NoSuchProcess:

            item["status"]="restarting"

            db_update(
                project,
                "restarting"
            )

            changed=True


    if changed:
        save(data)



if __name__=="__main__":

    print(
        "NONO Resource Monitor v2 Started"
    )

    while True:

        check()

        time.sleep(30)
