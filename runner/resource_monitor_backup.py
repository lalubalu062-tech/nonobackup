import os
import json
import time
import psutil
import signal

FILE="processes.json"

MAX_RAM_MB = 512


def kill_project(project_id, pid, data):

    try:
        os.kill(pid, signal.SIGTERM)

        data[str(project_id)]["status"]="killed"

        with open(FILE,"w") as f:
            json.dump(data,f,indent=2)

        print("Killed:", project_id)

    except Exception as e:
        print(e)


def check_resources():

    if not os.path.exists(FILE):
        return

    with open(FILE) as f:
        data=json.load(f)


    for project,p in data.items():

        pid=p["pid"]

        try:

            proc=psutil.Process(pid)

            memory=proc.memory_info().rss / 1024 / 1024
            cpu=proc.cpu_percent(interval=1)


            print(
                "Project:",
                project,
                "RAM:",
                round(memory,2),
                "MB CPU:",
                cpu
            )


            if memory > MAX_RAM_MB:
                kill_project(
                    project,
                    pid,
                    data
                )


        except psutil.NoSuchProcess:
            data[project]["status"]="stopped"


    with open(FILE,"w") as f:
        json.dump(data,f,indent=2)



if __name__=="__main__":

    print("NONO Resource Monitor Started")

    while True:
        check_resources()
        time.sleep(30)
