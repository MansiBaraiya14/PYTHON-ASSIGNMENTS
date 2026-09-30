import heapq


# Read number of workers and jobs
w, n = map(int, input().split())

jobs = []

for arrival_index in range(n):
    arrival, job_id, priority, duration, resources = input().split()

    jobs.append({
        "arrival": int(arrival),
        "job_id": job_id,
        "priority": int(priority),
        "duration": int(duration),
        "resources": int(resources),
        "order": arrival_index
    })


# Sort jobs by arrival time
jobs.sort(key=lambda x: (x["arrival"], x["order"]))


# Worker availability
# (available_time, worker_number)
workers = []

for i in range(1, w + 1):
    heapq.heappush(workers, (0, i))


# Waiting jobs:
# (-priority, arrival time, arrival order, job)
waiting = []

results = []

job_index = 0
current_time = 0
total_wait = 0


while job_index < n or waiting:

    # If no waiting job, move time to next arrival
    if not waiting and job_index < n:
        current_time = max(
            current_time,
            jobs[job_index]["arrival"]
        )

    # Add all jobs that have arrived
    while (
        job_index < n
        and jobs[job_index]["arrival"] <= current_time
    ):
        job = jobs[job_index]

        heapq.heappush(
            waiting,
            (
                -job["priority"],
                job["arrival"],
                job["order"],
                job
            )
        )

        job_index += 1

    # Get earliest available worker
    available_time, worker_number = heapq.heappop(workers)

    # If worker is not available yet
    if available_time > current_time:

        # Put worker back
        heapq.heappush(
            workers,
            (available_time, worker_number)
        )

        current_time = available_time
        continue

    # If no job is currently waiting
    if not waiting:

        heapq.heappush(
            workers,
            (available_time, worker_number)
        )

        continue

    # Highest priority job
    _, _, _, job = heapq.heappop(waiting)

    start_time = max(
        current_time,
        job["arrival"]
    )

    finish_time = start_time + job["duration"]

    wait_time = start_time - job["arrival"]

    total_wait += wait_time

    results.append(
        (
            job["job_id"],
            worker_number,
            start_time,
            finish_time
        )
    )

    # Worker becomes available at finish time
    heapq.heappush(
        workers,
        (finish_time, worker_number)
    )

    current_time = start_time


# Sort output by start time
results.sort(key=lambda x: (x[2], x[1]))

for job_id, worker, start, finish in results:
    print(
        job_id,
        "W" + str(worker),
        start,
        finish
    )


average_wait = total_wait / n

print(f"AVG_WAIT {average_wait:.2f}")