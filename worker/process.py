import subprocess
import signal
import socket
import os
import fcntl
import json
from datetime import datetime

BASE="/home/jeet/nono/projects"
PROCESS_FILE="/home/jeet/nono/runner/processes.json"
PROCESS_LOCK="/tmp/nono_process.lock"

def save_pid_file(project_id,pid):
    path=f"{BASE}/{project_id}/pid.json"
    with open(path,"w") as f:
        json.dump({
            "pid":pid,
            "status":"running",
            "started":str(datetime.utcnow())
        },f,indent=2)

def acquire_process_lock():
    f=open(PROCESS_LOCK,"w")
    try:
        fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        return f
    except:
        f.close()
        return None

def start(project_id,cmd):
    app_dir=f"{BASE}/{project_id}/app"
    log_file=f"{BASE}/{project_id}/logs/app.log"

    os.makedirs(os.path.dirname(log_file),exist_ok=True)

    if isinstance(cmd,str):
        cmd=cmd.split()

    print("LAUNCHING APP:",cmd)
    print("WORKDIR:",app_dir)

    log=open(log_file,"a",buffering=1)

    lock=acquire_process_lock()
    if not lock:
        raise Exception("PROCESS LOCK BUSY")

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

    save_pid_file(project_id,p.pid)

    print("APP PID:",p.pid)

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
        print("PORT SAVED",project_id,port)
    except Exception as e:
        print("PORT SAVE ERROR",e)


def wait_process(proc, timeout=600):
    try:
        proc.wait(timeout=timeout)
    except Exception:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except:
            pass


def get_free_port(start=8080,end=9000):
    for port in range(start,end):
        sock=socket.socket()
        try:
            sock.bind(("0.0.0.0",port))
            sock.close()
            return port
        except:
            sock.close()
    raise Exception("No free port available")
