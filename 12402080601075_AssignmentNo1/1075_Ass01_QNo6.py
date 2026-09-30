import heapq


# Read n and e
n, e = map(int, input().split())

modules = []

for _ in range(n):
    modules.append(input().strip())


# Graph
graph = {module: set() for module in modules}

# indegree[module] = number of dependencies
indegree = {module: 0 for module in modules}


# Read import relationships
for _ in range(e):
    a, b = input().split()

    # a imports b
    # Therefore b must be loaded before a
    if b not in graph[a]:
        graph[a].add(b)
        indegree[a] += 1


# Min-heap for lexicographically smallest module
heap = []

for module in modules:
    if indegree[module] == 0:
        heapq.heappush(heap, module)


order = []

while heap:

    current = heapq.heappop(heap)
    order.append(current)

    # Modules that depend on current
    for module in graph:
        if current in graph[module]:
            indegree[module] -= 1

            if indegree[module] == 0:
                heapq.heappush(heap, module)


# If all modules were loaded, no cycle
if len(order) == n:
    print(" ".join(order))

else:
    # Find one cycle using DFS
    state = {module: 0 for module in modules}
    parent = {}

    cycle = []

    def dfs(node):

        state[node] = 1

        for dependency in graph[node]:

            if state[dependency] == 0:
                parent[dependency] = node

                if dfs(dependency):
                    return True

            elif state[dependency] == 1:

                # Found a cycle
                cycle.append(dependency)

                current = node

                while current != dependency:
                    cycle.append(current)
                    current = parent[current]

                cycle.append(dependency)

                cycle.reverse()

                return True

        state[node] = 2
        return False

    for module in modules:
        if state[module] == 0:
            if dfs(module):
                break

    print("CYCLE")
    print(" ".join(cycle))