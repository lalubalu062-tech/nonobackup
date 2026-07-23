import os
import fcntl

LOCK_DIR="/tmp/nono_deploy_locks"
os.makedirs(LOCK_DIR,exist_ok=True)

def acquire(project_id):
    path=f"{LOCK_DIR}/{project_id}.lock"
    f=open(path,"w")
    try:
        fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        return f
    except:
        return None
