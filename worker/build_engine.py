import os
import subprocess
import time


def run_command(cmd,cwd,log):

    try:

        with open(log,"a") as f:

            p=subprocess.Popen(
                cmd,
                shell=True,
                cwd=cwd,
                stdout=f,
                stderr=subprocess.STDOUT
            )

            code=p.wait()

            return code==0


    except Exception as e:

        print(
            "BUILD CMD ERROR",
            e
        )

        return False



def build_project(job):

    project_id=job["id"]

    workspace=f"/home/jeet/nono/projects/{project_id}"

    app=f"{workspace}/app"

    log=f"{workspace}/logs/build.log"


    os.makedirs(
        app,
        exist_ok=True
    )


    print(
        "BUILD START",
        project_id
    )


    # python dependency

    req=f"{app}/requirements.txt"


    if os.path.exists(req):

        print(
            "Installing requirements"
        )

        ok=run_command(
            "pip install -r requirements.txt",
            app,
            log
        )


        if not ok:

            return False



    # node dependency

    package=f"{app}/package.json"


    if os.path.exists(package):

        print(
            "Installing npm packages"
        )

        ok=run_command(
            "npm install",
            app,
            log
        )


        if not ok:

            return False



    print(
        "BUILD COMPLETE",
        project_id
    )


    return True
