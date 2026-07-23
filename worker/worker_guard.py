import os
import signal
import atexit

LOCK_FILE="/tmp/nono-worker.lock"

def acquire_lock():
    if os.path.exists(LOCK_FILE):
        print("❌ Worker already running")
        exit(1)

    with open(LOCK_FILE,"w") as f:
        f.write(str(os.getpid()))

    print("🔒 Worker lock acquired")


def release_lock():
    try:
        os.remove(LOCK_FILE)
        print("🔓 Worker lock released")
    except:
        pass


def shutdown_handler(sig,frame):
    print("🛑 Shutdown signal received")
    release_lock()
    exit(0)


signal.signal(signal.SIGINT,shutdown_handler)
signal.signal(signal.SIGTERM,shutdown_handler)

atexit.register(release_lock)
