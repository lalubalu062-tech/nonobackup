import os
import json
import time

from runtime_detector import detect_runtime
from launcher import get_start_command


BASE="/home/jeet/nono/projects"


def deploy(job):

    project_id=job["id"]

    workspace=f"{BASE}/{project_id}"

    app_dir=f"{workspace}/app"

    log_dir=f"{workspace}/logs"


    os.makedirs(
        app_dir,
        exist_ok=True
    )

    os.makedirs(
        log_dir,
        exist_ok=True
    )


    meta={
        "id":project_id,
        "name":job.get("name"),
        "created":time.time()
    }


    with open(
        f"{workspace}/meta.json",
        "w"
    ) as f:
        json.dump(
            meta,
            f,
            indent=2
        )


    result=detect_runtime(app_dir)


    runtime=result["runtime"]
    cmd=result["command"]


    # empty local project
    if runtime=="unknown":

        main=f"{app_dir}/main.py"

        with open(main,"w") as f:

            f.write(
'''print("NONO APP RUNNING")
import time
while True:
    time.sleep(60)
'''
            )


        runtime="python"
        cmd="python3 -u main.py"



    print(
        "DETECTED:",
        runtime
    )

    print(
        "COMMAND:",
        cmd
    )


    job["runtime"]=runtime


    cmd,port=get_start_command(
        app_dir,
        cmd
    )


    if port:
        print(
            "PROJECT PORT:",
            port
        )


    return {
        "cmd": cmd,
        "port": port
    }
