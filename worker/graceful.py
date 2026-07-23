import signal
import sys

RUNNING=True

def stop(*args):
    global RUNNING
    print("🛑 Graceful shutdown...")
    RUNNING=False

signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

def alive():
    return RUNNING
