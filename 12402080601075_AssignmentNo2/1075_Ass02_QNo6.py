import re
from collections import defaultdict, deque


# Regex for log line
pattern = re.compile(
    r'^(\d{2}:\d{2})\s+(\S+)\s+(\S+)\s+(FAIL|SUCCESS)$'
)


def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes


# ---------------- INPUT ----------------

X, T = map(int, input().split())

n = int(input())

# Store failure timestamps and IPs for each user
failures = defaultdict(deque)

# Store first suspicious success
suspicious = {}


# ---------------- PROCESS LOGS ----------------

for _ in range(n):

    line = input().strip()

    match = pattern.match(line)

    if not match:
        continue

    timestamp, user, ip, status = match.groups()

    current_time = time_to_minutes(timestamp)

    # -------- FAILED LOGIN --------

    if status == "FAIL":

        failures[user].append(
            (current_time, ip)
        )

        # Remove failures outside T-minute window
        while (
            failures[user]
            and current_time - failures[user][0][0] > T
        ):
            failures[user].popleft()


    # -------- SUCCESSFUL LOGIN --------

    else:

        # Remove old failures
        while (
            failures[user]
            and current_time - failures[user][0][0] > T
        ):
            failures[user].popleft()

        # Check if there are at least X failures
        # from an IP different from the successful IP
        if len(failures[user]) >= X:

            different_ip = False

            for fail_time, fail_ip in failures[user]:

                if fail_ip != ip:
                    different_ip = True
                    break

            if different_ip and user not in suspicious:

                suspicious[user] = timestamp


# ---------------- OUTPUT ----------------

for user in sorted(suspicious):

    print(user, suspicious[user])