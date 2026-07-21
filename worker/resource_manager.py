import psutil
import time
import requests

from config import API_URL, WORKER_ID


MAX_RAM_MB = 512
MAX_CPU_PERCENT = 80


def check_process(pid):

    try:

        if not pid or not psutil.pid_exists(int(pid)):
            return {
                "status":"dead"
            }


        p = psutil.Process(int(pid))

        ram = round(
            p.memory_info().rss / 1024 / 1024,
            2
        )

        cpu = p.cpu_percent(
            interval=1
        )


        if ram > MAX_RAM_MB:

            return {
                "status":"limit",
                "reason":"ram",
                "ram":ram,
                "cpu":cpu
            }


        if cpu > MAX_CPU_PERCENT:

            return {
                "status":"limit",
                "reason":"cpu",
                "ram":ram,
                "cpu":cpu
            }


        return {
            "status":"ok",
            "ram":ram,
            "cpu":cpu
        }


    except Exception as e:

        return {
            "status":"error",
            "error":str(e)
        }



def get_projects():

    try:

        r=requests.get(
            f"{API_URL}/workers/{WORKER_ID}",
            timeout=5
        )

        return r.json().get(
            "projects",
            []
        )


    except Exception as e:

        print(
            "RESOURCE API ERROR:",
            e
        )

        return []



def restart_project(project_id):
    try:
        r=requests.post(
            f"{API_URL}/internal/projects/{project_id}/restart",
            timeout=5
        )
        print(
            "RESTART REQUEST:",
            project_id,
            r.text
        )
    except Exception as e:
        print(
            "RESTART ERROR:",
            e
        )


def monitor_resources():

    print(
        "Resource Manager Started"
    )


    while True:

        try:

            projects=get_projects()


            for project in projects:

                pid=project.get("pid")


                if pid:

                    result=check_process(pid)


                    if result["status"]!="ok":

                        print(
                            "RESOURCE LIMIT:",
                            project["id"],
                            result
                        )

                        restart_project(
                            project["id"]
                        )


        except Exception as e:

            print(
                "RESOURCE ERROR:",
                e
            )


        time.sleep(30)
