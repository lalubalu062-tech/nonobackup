import time
import os

print("NONO TEST APP STARTED", flush=True)

while True:
    print("APP ALIVE PID:", os.getpid(), flush=True)
    time.sleep(10)
