import os
import subprocess

repo = "https://github.com/psf/requests.git"
project_id = "test-project"

path = f"/home/jeet/nono/runner/workspace/{project_id}"

if not os.path.exists(path):
    print("Cloning repo...")
    subprocess.run(
        ["git", "clone", repo, path]
    )
else:
    print("Already cloned")

print("Done:", path)
