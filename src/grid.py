import random

import pygame

from src.colors import (
    BLACK,
    CLOSED,
    GREY,
    GREEN,
    OPEN,
    PATH,
    RED,
    TERRAIN_HIGH,
    TERRAIN_MEDIUM,
    VISITED,
    WHITE,
)


class Node:
    _cost_fonts = {}

    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.x = row * size
        self.y = col * size
        self.color = WHITE
        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.is_open = False
        self.is_closed = False
        self.is_visited = False
        self.is_path = False
        self.cost = 1
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def reset(self):
        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.is_open = False
        self.is_closed = False
        self.is_visited = False
        self.is_path = False
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.cost = 1
        self.color = WHITE

    def reset_search(self):
        self.is_open = False
        self.is_closed = False
        self.is_visited = False
        self.is_path = False
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

        if self.is_wall:
            self.color = BLACK
        elif self.is_start:
            self.color = GREEN
        elif self.is_end:
            self.color = RED
        elif self.cost == 3:
            self.color = TERRAIN_MEDIUM
        elif self.cost == 5:
            self.color = TERRAIN_HIGH
        else:
            self.color = WHITE

    def set_start(self):
        self.reset_search()
        self.is_wall = False
        self.is_start = True
        self.color = GREEN

    def set_end(self):
        self.reset_search()
        self.is_wall = False
        self.is_end = True
        self.color = RED

    def set_wall(self):
        self.reset_search()
        self.is_wall = True
        self.color = BLACK

    def cycle_cost(self):
        self.reset_search()
        self.is_wall = False
        self.cost = {1: 3, 3: 5, 5: 1}[self.cost]
        self._set_cost_color()

    def reset_cost(self):
        self.reset_search()
        self.is_wall = False
        self.cost = 1
        self.color = WHITE

    def _set_cost_color(self):
        if self.cost == 3:
            self.color = TERRAIN_MEDIUM
        elif self.cost == 5:
            self.color = TERRAIN_HIGH
        else:
            self.color = WHITE

    def set_open(self):
        if self.is_start or self.is_end or self.is_wall:
            return
        self.is_open = True
        self.color = OPEN

    def set_visited(self):
        if self.is_start or self.is_end or self.is_wall:
            return
        self.is_visited = True
        self.color = VISITED

    def set_closed(self):
        if self.is_start or self.is_end or self.is_wall:
            return
        self.is_closed = True
        self.color = CLOSED

    def set_path(self):
        if self.is_start or self.is_end or self.is_wall:
            return
        self.is_path = True
        self.color = PATH

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

        if self.cost > 1 and not self.is_wall and not self.is_start and not self.is_end:
            font_size = max(10, min(18, self.size // 2))
            font = self._cost_fonts.get(font_size)
            if font is None:
                font = pygame.font.SysFont("consolas", font_size, bold=True)
                self._cost_fonts[font_size] = font

            label = font.render(str(self.cost), True, BLACK)
            label_rect = label.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
            win.blit(label, label_rect)


class Grid:
    def __init__(self, rows, width):
        self.rows = rows
        self.width = width
        self.cell_size = width // rows
        self.grid = self._build_grid()
        self.start = None
        self.end = None

    def _build_grid(self):
        return [[Node(row, col, self.cell_size) for col in range(self.rows)] for row in range(self.rows)]

    def get_node(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.rows:
            return self.grid[row][col]
        return None

    def get_cell_from_mouse(self, position):
        x, y = position
        row = x // self.cell_size
        col = y // self.cell_size

        if 0 <= row < self.rows and 0 <= col < self.rows:
            return row, col
        return None, None

    def neighbors(self, node):
        row, col = node.row, node.col
        neighbors = []

        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row = row + dr
            next_col = col + dc
            candidate = self.get_node(next_row, next_col)
            if candidate is not None:
                neighbors.append(candidate)

        return neighbors

    def get_neighbors(self, node):
        return self.neighbors(node)

    def set_start(self, row, col):
        node = self.get_node(row, col)
        if node is None or node is self.end:
            return

        self.clear_search()

        if self.start is not None:
            self.start.reset_search()
            self.start.is_start = False
            self.start.color = WHITE

        node.set_start()
        self.start = node

    def set_end(self, row, col):
        node = self.get_node(row, col)
        if node is None or node is self.start:
            return

        self.clear_search()

        if self.end is not None:
            self.end.reset_search()
            self.end.is_end = False
            self.end.color = WHITE

        node.set_end()
        self.end = node

    def set_wall(self, row, col):
        node = self.get_node(row, col)
        if node is None:
            return

        if node is self.start or node is self.end:
            return

        self.clear_search()
        node.set_wall()

    def clear(self):
        for row in self.grid:
            for node in row:
                node.reset()
        self.start = None
        self.end = None

    def clear_search(self):
        for row in self.grid:
            for node in row:
                if node is self.start:
                    node.set_start()
                elif node is self.end:
                    node.set_end()
                elif not node.is_wall:
                    node.reset_search()
                    node.color = WHITE

    def generate_random_walls(self, density=0.28):
        for row in self.grid:
            for node in row:
                if node is self.start or node is self.end:
                    continue

                node.reset_search()
                node.is_wall = False
                if random.random() < density:
                    node.set_wall()
                else:
                    node._set_cost_color()

    def generate_random_maze(self, density=0.32):
        if self.rows < 2:
            raise ValueError("Random maze requires at least a 2x2 grid.")

        self.clear()

        start_row, start_col = random.randrange(self.rows), random.randrange(self.rows)
        max_distance = 2 * (self.rows - 1)
        minimum_distance = max(2, int(max_distance * 0.6))
        end_row, end_col = start_row, start_col

        for _ in range(1000):
            candidate_row = random.randrange(self.rows)
            candidate_col = random.randrange(self.rows)
            distance = abs(candidate_row - start_row) + abs(candidate_col - start_col)
            if distance >= minimum_distance:
                end_row, end_col = candidate_row, candidate_col
                break

        if (end_row, end_col) == (start_row, start_col):
            start_row, start_col = 0, 0
            end_row, end_col = self.rows - 1, self.rows - 1

        for row in self.grid:
            for node in row:
                if random.random() < density:
                    node.set_wall()

        primary_path = self._build_random_path(
            start_row,
            start_col,
            end_row,
            end_col,
        )
        alternative_neighbors = [
            (start_row + 1, start_col),
            (start_row - 1, start_col),
            (start_row, start_col + 1),
            (start_row, start_col - 1),
        ]
        alternative_neighbors = [
            position
            for position in alternative_neighbors
            if 0 <= position[0] < self.rows
            and 0 <= position[1] < self.rows
            and position != primary_path[1]
        ]
        alternative_start = random.choice(alternative_neighbors)
        alternative_path = [
            (start_row, start_col),
            *self._build_random_path(
                alternative_start[0],
                alternative_start[1],
                end_row,
                end_col,
            ),
        ]

        for row, col in set(primary_path + alternative_path):
            self._open_maze_cell(row, col)

        self.set_start(start_row, start_col)
        self.set_end(end_row, end_col)

    def _build_random_path(self, start_row, start_col, end_row, end_col):
        path = [(start_row, start_col)]
        current_row, current_col = start_row, start_col

        while (current_row, current_col) != (end_row, end_col):
            possible_steps = []
            if current_row < end_row:
                possible_steps.append((current_row + 1, current_col))
            elif current_row > end_row:
                possible_steps.append((current_row - 1, current_col))

            if current_col < end_col:
                possible_steps.append((current_row, current_col + 1))
            elif current_col > end_col:
                possible_steps.append((current_row, current_col - 1))

            current_row, current_col = random.choice(possible_steps)
            path.append((current_row, current_col))

        return path

    def _open_maze_cell(self, row, col):
        node = self.get_node(row, col)
        node.is_wall = False
        node.cost = 1
        node.reset_search()
        node.color = WHITE

    def clear_wall(self, row, col):
        node = self.get_node(row, col)
        if node is None or node is self.start or node is self.end:
            return

        self.clear_search()
        node.reset_search()
        node.is_wall = False
        node._set_cost_color()

    def set_cost(self, row, col):
        node = self.get_node(row, col)
        if node is None or node is self.start or node is self.end:
            return

        self.clear_search()
        node.cycle_cost()

    def reset_cost(self, row, col):
        node = self.get_node(row, col)
        if node is None or node is self.start or node is self.end:
            return

        self.clear_search()
        node.reset_cost()

    def draw(self, win):
        for row in self.grid:
            for node in row:
                node.draw(win)

        self._draw_lines(win)

    def _draw_lines(self, win):
        for i in range(self.rows + 1):
            pygame.draw.line(win, GREY, (0, i * self.cell_size), (self.width, i * self.cell_size))
            pygame.draw.line(win, GREY, (i * self.cell_size, 0), (i * self.cell_size, self.width))
