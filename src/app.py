import sys

import pygame

from src.algorithms import a_star, bfs, dfs, dijkstra
from src.colors import (
    ACCENT,
    BACKGROUND,
    BLACK,
    GREEN,
    PANEL,
    PANEL_MUTED,
    RED,
    TERRAIN_HIGH,
    TERRAIN_MEDIUM,
    WHITE,
)
from src.grid import Grid


class PathfindingVisualizer:
    def __init__(self, width=800, rows=20):
        pygame.init()
        self.width = width
        self.height = width + 136
        self.rows = rows
        self.screen = pygame.display.set_mode((width, self.height))
        pygame.display.set_caption("Pathfinding Visualizer")
        self.clock = pygame.time.Clock()
        self.grid = Grid(rows, width)
        self.mode = "wall"
        self.algorithm = "A*"
        self.running = False
        self.stop_requested = False
        self.status_message = "Select a mode and draw your grid."
        pygame.mouse.set_visible(False)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.mode = "start"
                    self.status_message = "Start mode selected."
                elif event.key == pygame.K_e:
                    self.mode = "end"
                    self.status_message = "End mode selected."
                elif event.key == pygame.K_w:
                    self.mode = "wall"
                    self.status_message = "Wall mode selected."
                elif event.key == pygame.K_1:
                    self.algorithm = "A*"
                elif event.key == pygame.K_2:
                    self.algorithm = "Dijkstra"
                elif event.key == pygame.K_3:
                    self.algorithm = "BFS"
                elif event.key == pygame.K_4:
                    self.algorithm = "DFS"
                elif event.key == pygame.K_t:
                    self.mode = "terrain"
                    self.status_message = "Terrain mode selected. Click to cycle costs 1 / 3 / 5."
                elif event.key == pygame.K_c:
                    self.grid.clear()
                    self.running = False
                    self.status_message = "Grid cleared."
                elif event.key == pygame.K_r:
                    self.grid.clear_search()
                    self.running = False
                    self.status_message = "Search reset."
                elif event.key == pygame.K_m:
                    self.grid.generate_random_maze()
                    self.running = False
                    self.status_message = "Random maze generated with a guaranteed path."
                elif event.key == pygame.K_SPACE:
                    self.run_algorithm()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.running:
                    continue

                row, col = self.grid.get_cell_from_mouse(event.pos)
                if row is None or col is None:
                    continue

                if self.mode == "start":
                    self.grid.set_start(row, col)
                elif self.mode == "end":
                    self.grid.set_end(row, col)
                elif self.mode == "wall" and event.button == 1:
                    self.grid.set_wall(row, col)
                elif self.mode == "wall" and event.button == 3:
                    self.grid.clear_wall(row, col)
                elif self.mode == "terrain" and event.button == 1:
                    self.grid.set_cost(row, col)
                elif self.mode == "terrain" and event.button == 3:
                    self.grid.reset_cost(row, col)

            if event.type == pygame.MOUSEMOTION and any(pygame.mouse.get_pressed()[:2]):
                if self.running:
                    continue

                row, col = self.grid.get_cell_from_mouse(event.pos)
                if row is None or col is None:
                    continue

                if self.mode == "wall" and pygame.mouse.get_pressed()[0]:
                    self.grid.set_wall(row, col)
                elif self.mode == "wall" and pygame.mouse.get_pressed()[2]:
                    self.grid.clear_wall(row, col)
                elif self.mode == "terrain" and pygame.mouse.get_pressed()[0]:
                    self.grid.set_cost(row, col)
                elif self.mode == "terrain" and pygame.mouse.get_pressed()[2]:
                    self.grid.reset_cost(row, col)

    def run_algorithm(self):
        if self.running:
            return

        if self.grid.start is None or self.grid.end is None:
            self.status_message = "Place both a start and an end point first."
            return

        self.running = True
        self.stop_requested = False
        self.grid.clear_search()
        algorithms = {
            "A*": a_star,
            "Dijkstra": dijkstra,
            "BFS": bfs,
            "DFS": dfs,
        }
        algorithm = algorithms[self.algorithm]
        path = algorithm(self.grid, self.draw, delay=20, stop_callback=self.should_stop)
        self.running = False

        if self.stop_requested:
            self.grid.clear_search()
            self.status_message = "Search stopped."
        else:
            self.status_message = (
                f"{self.algorithm} found a path with {len(path) - 1} steps."
                if path
                else f"{self.algorithm} could not find a path."
            )

    def should_stop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.stop_requested = True

        return self.stop_requested

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BACKGROUND)
        self.grid.draw(self.screen)
        self.draw_ui()
        self.draw_cursor()
        pygame.display.flip()

    def draw_cursor(self):
        if self.running:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if not (0 <= mouse_x < self.width and 0 <= mouse_y < self.width):
            return

        cursor_colors = {
            "wall": BLACK,
            "start": GREEN,
            "end": RED,
            "terrain": TERRAIN_HIGH,
        }
        color = cursor_colors[self.mode]

        pygame.draw.circle(self.screen, WHITE, (mouse_x, mouse_y), 9)
        pygame.draw.circle(self.screen, BLACK, (mouse_x, mouse_y), 7)
        pygame.draw.circle(self.screen, color, (mouse_x, mouse_y), 5)

    def draw_ui(self):
        panel_rect = pygame.Rect(0, self.width, self.width, self.height - self.width)
        pygame.draw.rect(self.screen, PANEL, panel_rect)

        title_font = pygame.font.SysFont("consolas", 17, bold=True)
        body_font = pygame.font.SysFont("consolas", 13)
        small_font = pygame.font.SysFont("consolas", 12)

        title = title_font.render("PATHFINDING LAB", True, WHITE)
        self.screen.blit(title, (22, self.width + 16))

        self.draw_badge(
            f"{self.algorithm.upper()}  [1-4]",
            (205, self.width + 14),
            ACCENT,
            small_font,
        )
        mode_colors = {
            "wall": BLACK,
            "start": GREEN,
            "end": RED,
            "terrain": TERRAIN_MEDIUM,
        }
        self.draw_badge(
            f"{self.mode.upper()}  [W/S/E/T]",
            (365, self.width + 14),
            mode_colors[self.mode],
            small_font,
        )

        controls = body_font.render(
            "SPACE run   ESC stop   M maze   R reset   C clear   RMB erase/cost",
            True,
            PANEL_MUTED,
        )
        self.screen.blit(controls, (22, self.width + 48))

        cost_legend = small_font.render(
            "TERRAIN COST:  1 white   3 orange   5 brown",
            True,
            PANEL_MUTED,
        )
        self.screen.blit(cost_legend, (22, self.width + 64))

        status = small_font.render(self.status_message, True, WHITE)
        self.screen.blit(status, (22, self.width + 88))

    def draw_badge(self, text, position, color, font):
        label = font.render(text, True, WHITE)
        badge = label.get_rect(topleft=position).inflate(18, 8)
        pygame.draw.rect(self.screen, color, badge, border_radius=5)
        self.screen.blit(label, position)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
