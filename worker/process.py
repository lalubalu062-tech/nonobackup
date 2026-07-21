import subprocess
import os
import json
import signal
import psutil
from container_manager import apply_limits
from datetime import datetime

BASE="/home/jeet/nono/projects"
PROCESS_FILE="/home/jeet/nono/runner/processes.json"

processes={}


def save_process(project_id,pid,status="running"):

    try:

        os.makedirs(
            os.path.dirname(PROCESS_FILE),
            exist_ok=True
        )

        data={}

        if os.path.exists(PROCESS_FILE):

            with open(PROCESS_FILE) as f:
                data=json.load(f)


        data[str(project_id)] = {
            "pid":pid,
            "status":status,
            "updated":str(datetime.utcnow())
        }


        with open(PROCESS_FILE,"w") as f:

            json.dump(
                data,
                f,
                indent=2
            )


    except Exception as e:

        print(
            "PROCESS SAVE ERROR",
            e
        )



def save_pid_file(project_id,pid):

    try:

        path=f"{BASE}/{project_id}/pid.json"

        data={
            "pid":pid,
            "status":"running",
            "started":str(datetime.utcnow())
        }


        with open(path,"w") as f:

            json.dump(
                data,
                f,
                indent=2
            )


    except Exception as e:

        print(
            "PID FILE ERROR",
            e
        )



def start(project_id,cmd):


    project_path=f"{BASE}/{project_id}"

    log_dir=f"{project_path}/logs"

    os.makedirs(
        log_dir,
        exist_ok=True
    )


    log_file=f"{log_dir}/app.log"


    log=open(
        log_file,
        "a",
        buffering=1
    )


    if isinstance(cmd,str):

        cmd=cmd.split()


    p=subprocess.Popen(

        cmd,

        stdout=log,

        stderr=subprocess.STDOUT,

        start_new_session=True,

        env={
            **os.environ,
            "PYTHONUNBUFFERED":"1"
        }

    )


    processes[project_id]=p.pid


    save_process(
        project_id,
        p.pid
    )


    save_pid_file(
        project_id,
        p.pid
    )


    print(
        "PROCESS STARTED",
        project_id,
        p.pid
    )


    apply_limits(
        project_id,
        p.pid
    )

    return p.pid



def stop(project_id):


    pid=processes.get(project_id)


    if not pid:

        try:

            with open(
                f"{BASE}/{project_id}/pid.json"
            ) as f:

                pid=json.load(f)["pid"]

        except:

            return False



    try:


        if psutil.pid_exists(pid):

            parent=psutil.Process(pid)


            for child in parent.children(
                recursive=True
            ):

                try:
                    child.kill()

                except:
                    pass


            try:

                parent.kill()

            except:
                pass



        try:

            os.killpg(
                os.getpgid(pid),
                signal.SIGKILL
            )

        except:

            pass



        save_process(
            project_id,
            pid,
            "stopped"
        )


        return True



    except Exception as e:

        print(
            "STOP ERROR",
            e
        )

        return False
