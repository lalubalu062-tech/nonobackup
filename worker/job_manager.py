from event_logger import log_event
import time
import requests

from config import API_URL, WORKER_ID, CHECK_INTERVAL
from process import start, save_port
from deploy import deploy
from tracer import trace
from build_engine import build_project
from git_engine import clone_repo


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
    trace(job["id"],"JOB_STARTED",job)

    print(
        "Preparing deploy:",
        job["id"]
    )

    try:

        print("STEP 1 CLONE")
        print("STEP CLONE START", job["id"])
        trace(job["id"],"CLONE_START")
        if not clone_repo(job):
            print("GIT CLONE FAILED")
            update_status(
                job["id"],
                "failed"
            )
            print("FAILED STEP TRACE:", job["id"])
            return

        print("STEP 2 BUILD")
        print("STEP BUILD START", job["id"])
        trace(job["id"],"CLONE_DONE")
        trace(job["id"],"BUILD_START")
        if not build_project(job):
            print("BUILD FAILED")
            update_status(
                job["id"],
                "failed"
            )
            print("FAILED STEP TRACE:", job["id"])
            return

        log_event(job["id"], "DEPLOY_START", job)
        print("STEP 3 DEPLOY")
        print("STEP DEPLOY START", job["id"])
        trace(job["id"],"BUILD_DONE")
        trace(job["id"],"DEPLOY_START")
        deploy_result = deploy(job)
        trace(job["id"],"DEPLOY_RESULT",deploy_result)
        print("DEPLOY RESULT", deploy_result)
        log_event(job["id"], "DEPLOY_RESULT", str(deploy_result))

        if not deploy_result:
            print(
                "No command generated"
            )
            return


        print("STEP 4 START PROCESS")
        print("STEP PROCESS START", deploy_result)
        trace(job["id"],"PROCESS_START")
        pid=start(
            job["id"],
            deploy_result["cmd"]
        )

        if deploy_result.get("port"):
            save_port(
                job["id"],
                deploy_result["port"]
            )

        trace(job["id"],"PROCESS_STARTED",pid)
        print(
            "Started:",
            pid
        )
        log_event(job["id"], "PROCESS_STARTED", pid)


        update_status(
            job["id"],
            "running",
            pid
        )


    except Exception as e:

        print("Deploy failed:", e)
        import traceback
        traceback.print_exc()

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

            print("POLLING JOBS")
            jobs=requests.get(
                f"{API_URL}/jobs",
                params={"worker_id": WORKER_ID},
                timeout=5
            ).json()


            print("JOBS FOUND:", jobs)
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
