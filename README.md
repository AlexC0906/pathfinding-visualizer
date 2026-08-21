# Pathfinding Visualizer

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2D_Engine-green.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)


A desktop pathfinding visualizer built with Python and Pygame. Draw walls, place start and end points, create weighted terrain, and watch different algorithms explore the grid in real time.

## Features

- **Interactive Pygame Grid:** Fully responsive 2D rendering.
- **Pathfinding Algorithms:** A*, Dijkstra, BFS, and DFS.
- **Dynamic Placement:** Set start and end points directly on the grid.
- **Obstacles:** Draw walls with mouse drag; remove them with right-click.
- **Weighted Terrain:** Add terrain with movement costs of `1`, `3`, and `5` (displayed directly inside grid cells).
- **Smart Maze Generation:** Random mazes guarantee at least two valid routes between distant start and end points.
- **Real-Time Animation:** Watch the search and path reconstruction live.
- **Responsive Controls:** Search cancellation (`ESC`), state reset, and complete grid reset.
- **Custom UI/UX:** Custom cursor showing the selected editing mode and a clean control panel with algorithm, mode, controls, and status feedback.

## Algorithms

### A*
A* uses the Manhattan distance heuristic to guide the search. It supports weighted terrain and finds a minimum-cost path.

### Dijkstra
Dijkstra explores the grid according to accumulated movement cost. It supports weighted terrain and guarantees the minimum-cost path.

### BFS (Breadth-First Search)
BFS explores the grid level by level and finds the path with the fewest steps. It ignores terrain costs.

### DFS (Depth-First Search)
DFS explores one branch deeply before backtracking. It can find a path, but does not guarantee the shortest or cheapest path.

## Terrain Costs

| Cost | Appearance | Meaning |
| :---: | :--- | :--- |
| `1` | White | Normal terrain |
| `3` | Orange | Medium-cost terrain |
| `5` | Brown | High-cost terrain |

*Note: Only A* and Dijkstra utilize terrain costs. BFS and DFS treat every walkable cell equally.*

## Controls

| Key / Action | Function |
| --- | --- |
| `1` / `2` / `3` / `4` | Select Algorithm (A* / Dijkstra / BFS / DFS) |
| `W` / `S` / `E` / `T` | Select Mode (Wall / Start / End / Terrain) |
| `SPACE` | Run the selected algorithm |
| `ESC` | Stop the current search |
| `M` | Generate a random maze |
| `R` / `C` | Reset search state / Clear entire grid |
| `Left Click` | Place, draw, or cycle the selected item |
| `Right Click` | Remove a wall or reset terrain to cost `1` |

## Setup

Install Python 3.9 or newer, then install Pygame:

```bash
python -m pip install pygame
