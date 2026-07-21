import os
import shutil
import subprocess


def clone_repo(repo, project_id):

    path = f"/home/jeet/nono/runner/workspace/{project_id}"

    if os.path.exists(path):
        print("Already exists:", path)
        return path


    # Local project support
    if repo.startswith("/"):
        print("Copying local project:", repo)

        shutil.copytree(
            repo,
            path
        )

        print("Copy success")
        return path


    # Git repository support
    print("Cloning:", repo)

    result = subprocess.run(
        ["git", "clone", repo, path],
        capture_output=True,
        text=True
    )


    if result.returncode == 0:
        print("Clone success")
        return path
    else:
        print("Clone failed")
        print(result.stderr)
        return None
