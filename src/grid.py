import pygame

from src.colors import BLACK, CLOSED, GREY, GREEN, OPEN, PATH, RED, VISITED, WHITE


class Node:
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
        else:
            self.color = WHITE

    def set_start(self):
        self.reset_search()
        self.is_start = True
        self.color = GREEN

    def set_end(self):
        self.reset_search()
        self.is_end = True
        self.color = RED

    def set_wall(self):
        self.reset_search()
        self.is_wall = True
        self.color = BLACK

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
        if node is None:
            return

        if self.start is not None:
            self.start.reset_search()
            self.start.is_start = False
            self.start.color = WHITE

        node.set_start()
        self.start = node

    def set_end(self, row, col):
        node = self.get_node(row, col)
        if node is None:
            return

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

    def draw(self, win):
        for row in self.grid:
            for node in row:
                node.draw(win)

        self._draw_lines(win)

    def _draw_lines(self, win):
        for i in range(self.rows + 1):
            pygame.draw.line(win, GREY, (0, i * self.cell_size), (self.width, i * self.cell_size))
            pygame.draw.line(win, GREY, (i * self.cell_size, 0), (i * self.cell_size, self.width))
