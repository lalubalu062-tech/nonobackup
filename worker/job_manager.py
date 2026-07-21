import time
import requests

from config import API_URL, WORKER_ID, CHECK_INTERVAL
from process import start
from deploy import deploy
from build_engine import build_project


def update_status(job_id,status,pid=None):

    try:
        requests.post(
            f"{API_URL}/jobs/{job_id}/status",
            params={
                "status":status,
                "pid":pid or 0
            },
            timeout=5
        )
    except Exception as e:
        print("status update error:",e)



def run_job(job):
    print("🔥 RUN_JOB CALLED:", job)

    print(
        "Preparing deploy:",
        job["id"]
    )

    try:

        if not build_project(job):
            print("BUILD FAILED")
            update_status(
                job["id"],
                "failed"
            )
            return

        cmd=deploy(job)

        if not cmd:
            print(
                "No command generated"
            )
            return


        pid=start(
            job["id"],
            cmd
        )

        print(
            "Started:",
            pid
        )


        update_status(
            job["id"],
            "running",
            pid
        )


    except Exception as e:

        print(
            "Deploy failed:",
            e
        )

        update_status(
            job["id"],
            "failed"
        )



def job_loop():

    print(
        "Job manager started"
    )


    while True:

        try:

            jobs=requests.get(
                f"{API_URL}/jobs",
                params={"worker_id": WORKER_ID},
                timeout=5
            ).json()


            for job in jobs:

                if job.get("status") in ["pending","restarting"]:

                    r=requests.post(
                        f"{API_URL}/jobs/{job['id']}/claim",
                        params={
                            "worker_id":WORKER_ID
                        },
                        timeout=5
                    )


                    print(
                        "Claim:",
                        r.text
                    )


                    if r.status_code==200:
                        print("CLAIM SUCCESS RUNNING DEPLOY", job["id"])
                        job["status"]="running"
                        run_job(job)


        except Exception as e:

            print(
                "Job loop error:",
                e
            )


        time.sleep(
            CHECK_INTERVAL
        )
