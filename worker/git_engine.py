import os
import subprocess


BASE="/home/jeet/nono/projects"


def clone_repo(job):

    repo=job.get("repo")

    if not repo:
        return True


    if repo=="local":
        return True


    project_id=job["id"]

    app_dir=f"{BASE}/{project_id}/app"


    os.makedirs(
        app_dir,
        exist_ok=True
    )


    print(
        "CLONING REPO:",
        repo
    )


    try:

        if os.listdir(app_dir):
            print(
                "APP DIR NOT EMPTY"
            )
            return True


        result=subprocess.run(
            [
                "git",
                "clone",
                repo,
                app_dir
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )


        print(
            result.stdout
        )


        if result.returncode!=0:

            print(
                "GIT CLONE FAILED"
            )

            return False


        print(
            "GIT CLONE SUCCESS"
        )

        return True


    except Exception as e:

        print(
            "GIT ERROR:",
            e
        )

        return False
