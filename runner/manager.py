import os
import json
import signal
from executor import run_project

FILE="processes.json"


def stop_process(project_id):

    with open(FILE) as f:
        data=json.load(f)

    project=str(project_id)

    if project not in data:
        return False

    pid=data[project]["pid"]

    try:
        os.kill(pid, signal.SIGTERM)
    except:
        pass

    data[project]["status"]="stopped"

    with open(FILE,"w") as f:
        json.dump(data,f,indent=2)

    return True



def restart_process(project_id):

    with open(FILE) as f:
        data=json.load(f)

    project=str(project_id)

    if project not in data:
        return False


    old=data[project]

    stop_process(project_id)

    print("Starting again...")

    process=run_project(
        old["path"],
        old["runtime"],
        project_id
    )

    if process:
        return {
            "id": project_id,
            "pid": process.pid,
            "status":"running"
        }

    return False
