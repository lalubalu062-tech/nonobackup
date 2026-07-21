import os
import psutil
import shutil


CGROUP="/sys/fs/cgroup"


DEFAULT_LIMITS={
    "memory":"512M",
    "cpu":"50%",
    "disk":"1G"
}


def check_cgroup():

    try:
        if os.path.exists(
            CGROUP+"/cgroup.controllers"
        ):
            return True

    except:
        pass

    return False



def apply_limits(project_id,pid):

    print(
        "CONTAINER SETUP",
        project_id,
        pid
    )


    if not check_cgroup():

        print(
        "CGROUP NOT AVAILABLE"
        )

        return {
            "mode":"fallback"
        }



    if not os.access(
        CGROUP,
        os.W_OK
    ):

        print(
        "CGROUP READ ONLY - FALLBACK MODE"
        )

        return {
            "mode":"monitor"
        }


    return {
        "mode":"cgroup",
        "memory":DEFAULT_LIMITS["memory"],
        "cpu":DEFAULT_LIMITS["cpu"],
        "disk":DEFAULT_LIMITS["disk"]
    }



def resource_policy(pid):

    try:

        p=psutil.Process(pid)

        return {
            "ram":
            round(
            p.memory_info().rss/1024/1024,
            2
            ),

            "cpu":
            p.cpu_percent(
                interval=0.2
            ),

            "disk":
            "monitor"
        }


    except:

        return {
            "status":"dead"
        }
