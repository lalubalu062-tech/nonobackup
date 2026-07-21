import os
from datetime import datetime

BASE="/home/jeet/nono/projects"

def trace(job_id, step, data=""):
    try:
        path=f"{BASE}/{job_id}/trace.log"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path,"a") as f:
            f.write(f"[{datetime.now()}] {step} :: {data}\n")
    except Exception as e:
        print("TRACE ERROR",e)
