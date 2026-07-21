import time

x = []

print("Memory test started")

while True:
    x.append("A" * 1024 * 1024 * 100)
    print("Allocated 100MB")
    time.sleep(5)
