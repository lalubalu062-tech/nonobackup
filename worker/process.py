import subprocess
import os
import json
from datetime import datetime

BASE="/home/jeet/nono/projects"
PROCESS_FILE="/home/jeet/nono/runner/processes.json"


def save_pid_file(project_id,pid):

    path=f"{BASE}/{project_id}/pid.json"

    with open(path,"w") as f:
        json.dump(
            {
                "pid":pid,
                "status":"running",
                "started":str(datetime.utcnow())
            },
            f,
            indent=2
        )


def start(project_id,cmd):

    app_dir=f"{BASE}/{project_id}/app"

    log_file=f"{BASE}/{project_id}/logs/app.log"

    os.makedirs(
        os.path.dirname(log_file),
        exist_ok=True
    )


    if isinstance(cmd,str):
        cmd=cmd.split()


    print(
        "LAUNCHING APP:",
        cmd
    )

    print(
        "WORKDIR:",
        app_dir
    )


    log=open(
        log_file,
        "a",
        buffering=1
    )


    p=subprocess.Popen(

        cmd,

        cwd=app_dir,

        stdout=log,

        stderr=subprocess.STDOUT,

        start_new_session=True,

        env={
            **os.environ,
            "PYTHONUNBUFFERED":"1"
        }

    )


    save_pid_file(
        project_id,
        p.pid
    )


    print(
        "APP PID:",
        p.pid
    )


    return p.pid

def save_port(project_id,port):
    import sqlite3
    try:
        db="/home/jeet/nono/backend/nono.db"
        conn=sqlite3.connect(db)
        cur=conn.cursor()
        cur.execute(
            "UPDATE projects SET port=? WHERE id=?",
            (port,project_id)
        )
        conn.commit()
        conn.close()
        print(
            "PORT SAVED",
            project_id,
            port
        )
    except Exception as e:
        print(
            "PORT SAVE ERROR",
            e
        )
