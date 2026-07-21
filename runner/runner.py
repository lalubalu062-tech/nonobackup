import time
import requests
import socket
from clone import clone_repo
from runtime import detect_runtime
from executor import run_project

API="http://127.0.0.1:8001"
WORKER_ID="node-"+socket.gethostname()

print("NONO Runner Started:", WORKER_ID)

while True:
    try:
        jobs=requests.get(
            f"{API}/jobs"
        ).json()

        for job in jobs:
            print("Found:", job["id"], job["name"])

            claim=requests.post(
                f"{API}/jobs/{job['id']}/claim",
                params={
                    "worker_id":WORKER_ID
                }
            ).json()

            print("Claim:", claim)

            if claim.get("status")=="running":

                path=clone_repo(
                    job["repo"],
                    job["id"]
                )

                print("Clone:", path)

                if path:
                    runtime=detect_runtime(path)

                    print("Runtime:",runtime)

                    process=run_project(
                        path,
                        runtime,
                        job["id"]
                    )

                    if process:
                        print(
                            "Started PID:",
                            process.pid
                        )

            time.sleep(2)

        time.sleep(5)

    except Exception as e:
        print("ERROR:",e)
        time.sleep(5)
