import os
import json
import subprocess


PROCESS_FILE = "processes.json"


def save_process(project_id, pid, runtime, path):

    data = {}

    if os.path.exists(PROCESS_FILE):
        with open(PROCESS_FILE) as f:
            data = json.load(f)

    data[str(project_id)] = {
        "pid": pid,
        "runtime": runtime,
        "path": path,
        "status": "running"
    }

    with open(PROCESS_FILE, "w") as f:
        json.dump(data, f, indent=2)



def run_project(path, runtime, project_id):

    print("Starting:", runtime)

    process = None


    if runtime == "python":

        if os.path.exists(os.path.join(path,"main.py")):
            cmd = ["python3","main.py"]

        elif os.path.exists(os.path.join(path,"app.py")):
            cmd = ["python3","app.py"]

        else:
            print("No main.py/app.py found")
            return None

        log_file = open(
            f"logs/{project_id}.log",
            "w"
        )

        process = subprocess.Popen(
            cmd,
            cwd=path,
            stdout=log_file,
            stderr=subprocess.STDOUT
        )



    elif runtime == "node":

        process = subprocess.Popen(
            ["npm", "start"],
            cwd=path
        )


    elif runtime == "php":

        process = subprocess.Popen(
            ["php", "-S", "0.0.0.0:8000"],
            cwd=path
        )


    if process:
        save_process(
            project_id,
            process.pid,
            runtime,
            path
        )

        return process


    print("Unsupported runtime")
    return None
