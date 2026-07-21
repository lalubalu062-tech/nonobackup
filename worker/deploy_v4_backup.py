import os
import json
import time
import subprocess
import shutil


BASE="/home/jeet/nono/projects"


def run(cmd,cwd=None):

    print("RUN:",cmd)

    return subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )


def detect_runtime(app):

    if os.path.exists(f"{app}/requirements.txt"):
        return "python"

    if os.path.exists(f"{app}/package.json"):
        return "node"

    if os.path.exists(f"{app}/main.py"):
        return "python"

    if os.path.exists(f"{app}/app.js"):
        return "node"

    return None



def clone_repo(repo,app):

    if repo in [
        "local",
        "",
        None
    ]:
        return True


    if os.path.exists(app):

        shutil.rmtree(app)


    os.makedirs(
        app,
        exist_ok=True
    )


    result=run(
        f"git clone {repo} {app}"
    )


    if result.returncode!=0:

        print(result.stdout)

        return False


    return True



def install_dependencies(runtime,app):


    if runtime=="python":

        req=f"{app}/requirements.txt"

        if os.path.exists(req):

            run(
                f"pip3 install -r {req}"
            )


    if runtime=="node":

        if os.path.exists(
            f"{app}/package.json"
        ):

            run(
                "npm install",
                app
            )



def deploy(job):


    project_id=job["id"]

    workspace=f"{BASE}/{project_id}"

    app=f"{workspace}/app"

    logs=f"{workspace}/logs"


    os.makedirs(
        workspace,
        exist_ok=True
    )

    os.makedirs(
        logs,
        exist_ok=True
    )


    repo=job.get(
        "repo",
        "local"
    )


    if not os.path.exists(app):

        os.makedirs(app)



    if repo not in [
        "local",
        "",
        None
    ]:

        if not clone_repo(
            repo,
            app
        ):

            return None



    runtime=job.get(
        "runtime"
    )


    detected=detect_runtime(app)


    if detected:

        runtime=detected



    install_dependencies(
        runtime,
        app
    )



    meta={

        "id":project_id,
        "name":job.get("name"),
        "runtime":runtime,
        "repo":repo,
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



    if runtime=="python":

        if os.path.exists(
            f"{app}/main.py"
        ):

            cmd=f"python3 -u {app}/main.py"

        elif os.path.exists(
            f"{app}/app.py"
        ):

            cmd=f"python3 -u {app}/app.py"

        else:

            return None



    elif runtime=="node":

        cmd=f"node {app}/app.js"


    else:

        print(
            "Runtime not found"
        )

        return None



    print(
        "WORKSPACE:",
        workspace
    )

    print(
        "RUNTIME:",
        runtime
    )

    print(
        "CMD:",
        cmd
    )


    return cmd
