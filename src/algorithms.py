import heapq


def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)


def reconstruct_path(current_node):
    path = []
    while current_node is not None:
        path.append(current_node)
        current_node = current_node.parent
    return path[::-1]


def a_star(grid, draw_callback, delay=10):
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
        _, _, current = heapq.heappop(open_set)
        in_open_set.remove(current)

        if current is grid.end:
            path = reconstruct_path(current)
            for node in path:
                if node is not grid.start and node is not grid.end:
                    node.set_path()
                draw_callback()
            return path

        if current is not grid.start:
            current.set_closed()

        for neighbor in grid.get_neighbors(current):
            if neighbor.is_wall:
                continue

            tentative_g_score = g_score[current] + 1
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

        if delay:
            import pygame
            pygame.time.delay(delay)

    return []
