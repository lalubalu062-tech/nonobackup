from worker_guard import acquire_lock
import threading
from graceful import alive
from cleanup_manager import clean
from restart_queue import restart_loop
from status_sync import status_sync
acquire_lock()
threading.Thread(target=clean,daemon=True).start()
threading.Thread(target=restart_loop,daemon=True).start()
threading.Thread(target=status_sync,daemon=True).start()

import threading
from graceful import alive
import time

from heartbeat import heartbeat
from monitor import monitor
from job_manager import job_loop
from lifecycle import lifecycle
from health_manager import check_health
from migration import migration
from resource_manager import monitor_resources


print("NONO Worker v10 Started")


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

while alive():
    time.sleep(60)
