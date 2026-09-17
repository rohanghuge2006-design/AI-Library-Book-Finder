from collections import deque
import time


def bfs_search(graph, start_node, target):
    start_time = time.perf_counter()

    queue = deque()
    queue.append((start_node, [start_node]))

    visited = set()
    visited_order = []

    while queue:
        current, path = queue.popleft()

        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)

        if current.lower() == target.lower():
            end_time = time.perf_counter()

            return {
                "found": True,
                "path": path,
                "visited": visited_order,
                "nodes_visited": len(visited_order),
                "path_length": len(path),
                "execution_time": round(
                    (end_time - start_time) * 1000, 4
                )
            }

        for neighbour in graph.get(current, []):
            if neighbour not in visited:
                queue.append(
                    (neighbour, path + [neighbour])
                )

    end_time = time.perf_counter()

    return {
        "found": False,
        "path": [],
        "visited": visited_order,
        "nodes_visited": len(visited_order),
        "path_length": 0,
        "execution_time": round(
            (end_time - start_time) * 1000, 4
        )
    }