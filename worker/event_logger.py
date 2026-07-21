import os
import time
import json

BASE="/home/jeet/nono/projects"


def log_event(project_id,event,data=None):

    folder=f"{BASE}/{project_id}/logs"
    os.makedirs(folder,exist_ok=True)

    item={
        "time":time.time(),
        "event":event,
        "data":data
    }

    with open(
        f"{folder}/events.log",
        "a"
    ) as f:
        f.write(
            json.dumps(item)+"\n"
        )

    print(
        "EVENT",
        project_id,
        event,
        data
    )
