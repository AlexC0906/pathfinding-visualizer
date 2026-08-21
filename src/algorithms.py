import heapq
from collections import deque


def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)


def reconstruct_path(current_node):
    path = []
    while current_node is not None:
        path.append(current_node)
        current_node = current_node.parent
    return path[::-1]


def a_star(grid, draw_callback, delay=10, stop_callback=None):
    if grid.start is None or grid.end is None:
        return []

    open_set = []
    in_open_set = set()
    heapq.heappush(open_set, (0, 0, grid.start))
    in_open_set.add(grid.start)

    came_from = {}
    g_score = {grid.start: 0}
    grid.start.g = 0
    grid.start.h = heuristic(grid.start, grid.end)
    grid.start.f = grid.start.h

    counter = 1

    while open_set:
        if _should_stop(stop_callback):
            return []

        _, _, current = heapq.heappop(open_set)
        in_open_set.remove(current)

        if current is grid.end:
            path = reconstruct_path(current)
            for node in path:
                if _should_stop(stop_callback):
                    return []
                if node is not grid.start and node is not grid.end:
                    node.set_path()
                draw_callback()
            return path

        if current is not grid.start:
            current.set_closed()

        for neighbor in grid.get_neighbors(current):
            if neighbor.is_wall:
                continue

            tentative_g_score = g_score[current] + neighbor.cost
            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                neighbor.parent = current
                neighbor.g = tentative_g_score
                neighbor.h = heuristic(neighbor, grid.end)
                neighbor.f = neighbor.g + neighbor.h

                if neighbor not in in_open_set:
                    neighbor.set_open()
                    heapq.heappush(open_set, (neighbor.f, counter, neighbor))
                    in_open_set.add(neighbor)
                    counter += 1

        if current is not grid.start:
            current.set_visited()

        draw_callback()

        _delay(delay, stop_callback)

    return []


def dijkstra(grid, draw_callback, delay=10, stop_callback=None):
    if grid.start is None or grid.end is None:
        return []

    distances = {grid.start: 0}
    open_set = [(0, 0, grid.start)]
    visited = set()
    counter = 1

    while open_set:
        if _should_stop(stop_callback):
            return []

        distance, _, current = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)

        if current is grid.end:
            path = reconstruct_path(current)
            for node in path:
                if _should_stop(stop_callback):
                    return []
                if node is not grid.start and node is not grid.end:
                    node.set_path()
                draw_callback()
            return path

        if current is not grid.start:
            current.set_closed()

        for neighbor in grid.get_neighbors(current):
            if neighbor.is_wall or neighbor in visited:
                continue

            next_distance = distance + neighbor.cost
            if next_distance < distances.get(neighbor, float("inf")):
                distances[neighbor] = next_distance
                neighbor.parent = current
                neighbor.g = next_distance
                neighbor.set_open()
                heapq.heappush(open_set, (next_distance, counter, neighbor))
                counter += 1

        if current is not grid.start:
            current.set_visited()

        draw_callback()

        _delay(delay, stop_callback)

    return []


def bfs(grid, draw_callback, delay=10, stop_callback=None):
    if grid.start is None or grid.end is None:
        return []

    queue = deque([grid.start])
    visited = {grid.start}

    while queue:
        if _should_stop(stop_callback):
            return []

        current = queue.popleft()

        if current is grid.end:
            return _animate_path(current, draw_callback, stop_callback)

        if current is not grid.start:
            current.set_closed()

        for neighbor in grid.get_neighbors(current):
            if neighbor.is_wall or neighbor in visited:
                continue

            visited.add(neighbor)
            neighbor.parent = current
            neighbor.set_open()
            queue.append(neighbor)

        if current is not grid.start:
            current.set_visited()

        draw_callback()
        _delay(delay, stop_callback)

    return []


def dfs(grid, draw_callback, delay=10, stop_callback=None):
    if grid.start is None or grid.end is None:
        return []

    stack = [grid.start]
    visited = {grid.start}

    while stack:
        if _should_stop(stop_callback):
            return []

        current = stack.pop()

        if current is grid.end:
            return _animate_path(current, draw_callback, stop_callback)

        if current is not grid.start:
            current.set_closed()

        neighbors = list(reversed(grid.get_neighbors(current)))
        for neighbor in neighbors:
            if neighbor.is_wall or neighbor in visited:
                continue

            visited.add(neighbor)
            neighbor.parent = current
            neighbor.set_open()
            stack.append(neighbor)

        if current is not grid.start:
            current.set_visited()

        draw_callback()
        _delay(delay, stop_callback)

    return []


def _animate_path(current, draw_callback, stop_callback=None):
    path = reconstruct_path(current)
    for node in path:
        if _should_stop(stop_callback):
            return []
        if node is not current and not node.is_start:
            node.set_path()
        draw_callback()
    return path


def _should_stop(stop_callback):
    return stop_callback is not None and stop_callback()


def _delay(delay, stop_callback=None):
    if delay:
        import pygame
        pygame.time.delay(delay)
