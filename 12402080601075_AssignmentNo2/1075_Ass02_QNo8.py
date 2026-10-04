MOD = 1000000007

n, m = map(int, input().split())

# DP arrays for current row
max_score = [None] * m
path_count = [0] * m

for i in range(n):
    row = input().split()

    new_score = [None] * m
    new_count = [0] * m

    for j in range(m):

        # Blocked cell
        if row[j] == "X":
            continue

        value = int(row[j])

        # Starting cell
        if i == 0 and j == 0:
            new_score[j] = value
            new_count[j] = 1
            continue

        candidates = []

        # From top
        if max_score[j] is not None:
            candidates.append((max_score[j], path_count[j]))

        # From left
        if j > 0 and new_score[j - 1] is not None:
            candidates.append(
                (new_score[j - 1], new_count[j - 1])
            )

        # From diagonal
        if j > 0 and max_score[j - 1] is not None:
            candidates.append(
                (max_score[j - 1], path_count[j - 1])
            )

        # No valid path to this cell
        if not candidates:
            continue

        best = max(score for score, count in candidates)

        count = 0
        for score, paths in candidates:
            if score == best:
                count = (count + paths) % MOD

        new_score[j] = best + value
        new_count[j] = count

    max_score = new_score
    path_count = new_count


# Destination unreachable
if max_score[m - 1] is None:
    print("IMPOSSIBLE")
else:
    print(max_score[m - 1], path_count[m - 1])