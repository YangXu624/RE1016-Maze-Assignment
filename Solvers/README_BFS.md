# BreadthFirstSearch Solver Documentation

This folder contains the **BreadthFirstSearch.py** script, which implements a BFS algorithm to solve pathfinding in a grid-based maze. It generates a GIF visualization of the solving process.

## 🚀 What It Does

1.  **Reads Maze Data**: Imports the grid structure (walls vs paths), start point, end point, and item locations (like Hearts) from `maze_data_generated_mazemate.py`.
2.  **Solves the Maze**: Uses a Breadth-First Search algorithm to find the shortest path from point A to point B.
3.  **Visualizes**: Creates an animated GIF showing the "flood fill" exploration and the final path trace.

## 🛠 Recent Changes (Refactoring)

The script was recently updated to be more **modular** and **student-friendly** for teaching purposes.

### 1. New `solve_bfs` Function
*   **Old Behavior**: The BFS logic was hardcoded to run once from Start to End.
*   **New Behavior**: The logic is now encapsulated in `def solve_bfs(maze, start, end):`.
*   **Benefit**: You can call this function multiple times in a single run. This enables complex "multi-stage" goals, like "Go to key, then go to door".

### 2. Coordinate System Fix
*   **Old Behavior**: The script mixed up `(x, y)` vs `(row, col)`, leading to confusion or crashes with non-square mazes.
*   **New Behavior**: It correctly unpacks `(x, y)` tuples (where `x=col`, `y=row`) to match the standard Cartesian system used by the maze generator.

### 3. Integrated Data Source
*   **Old Behavior**: Used a manually typed 2D array in the script.
*   **New Behavior**: Imports `maze_grid` directly from `maze_data_generated_mazemate.py`. This ensures it solves the *actual* maze from the game/web tool.

## 🎮 How to Use (with Demo Scenarios)

The script is currently set up to demonstrate two scenarios automatically when run:

1.  **Direct Path (Default)**:
    *   Finds the shortest path from `Start` to `Goal`.
    *   Ignores any optional items.
    *   **Output**: `maze_sols/default_bfs_sol.gif`

2.  **Detour Path (Challenge)**:
    *   Demonstrates how to visit an optional item (Heart) that is *not* on the direct path.
    *   **Logic**:
        1.  Calls `solve_bfs(start, heart)`
        2.  Calls `solve_bfs(heart, end)`
        3.  Concatenates the results.
    *   **Output**: `maze_sols/heart_bfs_sol.gif`

## 📦 Setup & Running

This project uses **uv** for dependency management.

1.  **Install uv** (if not installed):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Run the script**:
    ```bash
    uv run BreadthFirstSearch.py
    ```
    *This will automatically read the dependencies (Pillow) and run the solver.*

---
*Original visualization code by Timur Bakibayev.*
