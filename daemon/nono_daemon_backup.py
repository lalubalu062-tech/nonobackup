import time
import subprocess
import socket


services = [
    {
        "name": "backend",
        "cmd": [
            "/home/jeet/nono/backend/venv/bin/uvicorn",
            "main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8001"
        ],
        "cwd": "/home/jeet/nono/backend"
    },
    {
        "name": "runner",
        "cmd": [
            "python3",
            "runner.py"
        ],
        "cwd": "/home/jeet/nono/runner"
    },
    {
        "name": "resource_monitor",
        "cmd": [
            "python3",
            "resource_monitor.py"
        ],
        "cwd": "/home/jeet/nono/runner"
    }
]


processes = {}


def port_ready(host, port):

    try:
        s = socket.create_connection(
            (host, port),
            timeout=2
        )
        s.close()
        return True

    except:
        return False



def start_service(service):

    name = service["name"]

    print("Starting:", name)

    proc = subprocess.Popen(
        service["cmd"],
        cwd=service["cwd"]
    )

    processes[name] = proc

    print(
        name,
        "PID:",
        proc.pid
    )



def check_service(service):

    name = service["name"]

    proc = processes.get(name)

    if proc is None:
        start_service(service)
        return


    if proc.poll() is not None:

        print(
            name,
            "stopped. Restarting..."
        )

        start_service(service)



def main():

    print(
        "NONO Recovery Daemon Started"
    )


    # Backend first

    start_service(
        services[0]
    )


    while not port_ready(
        "127.0.0.1",
        8001
    ):

        print(
            "Waiting backend..."
        )

        time.sleep(2)


    print(
        "Backend ready"
    )


    start_service(
        services[1]
    )

    start_service(
        services[2]
    )


    while True:

        for service in services:

            check_service(
                service
            )

        time.sleep(10)



if __name__ == "__main__":

    main()
