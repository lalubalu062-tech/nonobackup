import os
import signal
import psutil
import subprocess
import time


def is_running(pid):
    try:
        return psutil.pid_exists(int(pid))
    except:
        return False


def get_process_info(pid):
    try:
        p = psutil.Process(int(pid))

        return {
            "pid": pid,
            "status": p.status(),
            "cpu": p.cpu_percent(interval=0.1),
            "ram": round(
                p.memory_info().rss / 1024 / 1024,
                2
            )
        }

    except Exception:
        return {
            "pid": pid,
            "status": "dead",
            "cpu": 0,
            "ram": 0
        }


def start_process(cmd, log_file=None):

    stdout = subprocess.PIPE

    if log_file:
        stdout = open(
            log_file,
            "a",
            buffering=1
        )

    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=stdout,
        stderr=subprocess.STDOUT,
        start_new_session=True,
        env={
            **os.environ,
            "PYTHONUNBUFFERED":"1"
        }
    )

    return proc.pid


def kill_process(pid):

    try:

        pid=int(pid)

        if not psutil.pid_exists(pid):
            return True


        parent=psutil.Process(pid)


        # kill child processes
        for child in parent.children(
            recursive=True
        ):
            try:
                child.kill()
            except:
                pass


        # kill main process
        try:
            parent.kill()
        except:
            pass


        # kill process group
        try:
            os.killpg(
                os.getpgid(pid),
                signal.SIGKILL
            )
        except:
            pass


        time.sleep(1)


        return not psutil.pid_exists(pid)


    except Exception as e:

        print(
            "KILL ERROR:",
            e
        )

        return False
