import os
import json
import time

FILE="processes.json"


def check_processes():

    if not os.path.exists(FILE):
        return

    with open(FILE) as f:
        data=json.load(f)

    changed=False

    for project,p in data.items():

        pid=p["pid"]

        if os.path.exists(f"/proc/{pid}"):
            if p["status"] != "running":
                p["status"]="running"
                changed=True

        else:
            if p["status"] != "stopped":
                p["status"]="stopped"
                changed=True

    if changed:
        with open(FILE,"w") as f:
            json.dump(data,f,indent=2)


if __name__=="__main__":

    print("NONO Monitor Started")

    while True:
        check_processes()
        time.sleep(30)
