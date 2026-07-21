import os
import json
import time

BASE="/home/jeet/nono/projects"


def deploy(job):

    project_id = job["id"]
    runtime = job.get("runtime","python")

    workspace = f"{BASE}/{project_id}"

    app_dir = f"{workspace}/app"
    log_dir = f"{workspace}/logs"


    os.makedirs(
        app_dir,
        exist_ok=True
    )

    os.makedirs(
        log_dir,
        exist_ok=True
    )


    meta = {
        "id": project_id,
        "name": job.get("name"),
        "runtime": runtime,
        "created": time.time()
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


    if runtime=="python":

        main_file=f"{app_dir}/main.py"


        if not os.path.exists(main_file):

            with open(main_file,"w") as f:

                f.write(
'''print("NONO APP RUNNING")

import time

while True:
    time.sleep(60)
'''
                )


        cmd=f"python3 -u {main_file}"


    elif runtime=="node":

        cmd=f"node {app_dir}/app.js"


    else:

        print(
            "UNKNOWN RUNTIME",
            runtime
        )

        return None


    print(
        "Workspace:",
        workspace
    )

    print(
        "Runtime:",
        runtime
    )

    print(
        "CMD:",
        cmd
    )


    return cmd
