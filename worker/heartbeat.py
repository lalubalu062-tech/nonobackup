import time
import requests
import psutil
import socket
import sqlite3

from config import API_URL, WORKER_ID


def get_projects():

    try:
        c=sqlite3.connect(
            "/home/jeet/nono/backend/nono.db"
        )

        count=c.execute(
            "SELECT COUNT(*) FROM projects WHERE worker_id=? AND status='running'",
            (WORKER_ID,)
        ).fetchone()[0]

        c.close()

        return count

    except Exception:
        return 0


def heartbeat():

    data={
        "worker_id":WORKER_ID,
        "cpu":psutil.cpu_percent(),
        "ram":psutil.virtual_memory().percent,
        "projects":get_projects(),
        "hostname":socket.gethostname()
    }

    try:

        r=requests.post(
            f"{API_URL}/workers/heartbeat",
            json=data,
            timeout=5
        )

        print(
            "heartbeat:",
            r.text
        )

    except Exception as e:
        print(
            "heartbeat error:",
            e
        )


if __name__=="__main__":

    print("Heartbeat started")

    while True:
        heartbeat()
        time.sleep(30)
