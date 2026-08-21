import sys

import pygame

from src.algorithms import a_star
from src.colors import BACKGROUND
from src.grid import Grid


class PathfindingVisualizer:
    def __init__(self, width=800, rows=20):
        pygame.init()
        self.width = width
        self.height = width + 120
        self.rows = rows
        self.screen = pygame.display.set_mode((width, self.height))
        pygame.display.set_caption("Pathfinding Visualizer")
        self.clock = pygame.time.Clock()
        self.grid = Grid(rows, width)
        self.mode = "wall"
        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.mode = "start"
                elif event.key == pygame.K_e:
                    self.mode = "end"
                elif event.key == pygame.K_w:
                    self.mode = "wall"
                elif event.key == pygame.K_c:
                    self.grid.clear()
                    self.running = False
                elif event.key == pygame.K_r:
                    self.grid.clear_search()
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.run_algorithm()

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = self.grid.get_cell_from_mouse(event.pos)
                if row is None or col is None:
                    continue

                if self.mode == "start":
                    self.grid.set_start(row, col)
                elif self.mode == "end":
                    self.grid.set_end(row, col)
                elif self.mode == "wall":
                    self.grid.set_wall(row, col)

            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if self.running:
                    continue

                row, col = self.grid.get_cell_from_mouse(event.pos)
                if row is None or col is None:
                    continue

                if self.mode == "wall":
                    self.grid.set_wall(row, col)

    def run_algorithm(self):
        if self.running:
            return

        if self.grid.start is None or self.grid.end is None:
            return

        self.running = True
        self.grid.clear_search()
        a_star(self.grid, self.draw, delay=20)
        self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BACKGROUND)
        self.grid.draw(self.screen)
        self.draw_ui()
        pygame.display.flip()

    def draw_ui(self):
        font = pygame.font.SysFont("arial", 16)
        legend = [
            "Mode: wall (W) | start (S) | end (E) | clear (C) | reset search (R)",
            "Run algorithm: SPACE | Drag mouse to paint walls.",
        ]

        for i, text in enumerate(legend):
            label = font.render(text, True, (40, 40, 40))
            self.screen.blit(label, (20, self.width + 20 + i * 24))

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
