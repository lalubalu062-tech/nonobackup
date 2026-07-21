import threading
import time

from heartbeat import heartbeat
from monitor import monitor
from job_manager import job_loop
from lifecycle import lifecycle
from health_manager import check_health
from migration import migration
from resource_manager import monitor_resources


print("NONO Worker v5 Started")


threads = [

    heartbeat,

    monitor,

    job_loop,

    monitor_resources

]


for func in threads:

    threading.Thread(
        target=func,
        daemon=True
    ).start()



threading.Thread(
    target=lifecycle,
    daemon=True
).start()

threading.Thread(
    target=check_health,
    daemon=True
).start()

threading.Thread(
    target=migration,
    daemon=True
).start()

while True:
    time.sleep(60)
