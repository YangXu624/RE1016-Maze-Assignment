"""
Source code modified from:
How to Solve a Maze using BFS in Python by Timur Bakibayev:
https://levelup.gitconnected.com/solve-a-maze-with-python-e9f0580979a1
"""

from PIL import Image, ImageDraw
import maze_data_generated_mazemate as maze_data
import itertools
import copy

monster_stats = {
    "Bat": {"damage": 20, "freq": 1},
    "Ghost": {"damage": 20, "freq": 2},
    "SkeletonArcher": {"damage": 20, "freq": 2},
    "Skeleton": {"damage": 20, "freq": 2},
    "SkeletonKnight": {"damage": 20, "freq": 2},
    "Plant": {"damage": 30, "freq": 1},
    "DeathKnight": {"damage": 30, "freq": 2},
    "Golem": {"damage": 30, "freq": 2},
    "Cactus": {"damage": 20, "freq": 3},
    "Dragon": {"damage": 60, "freq": 1}
}

# Define weights for each objective
gem_score = 1000
hp_score = 8
step_score = 50

import heapq

def solve_dijkstra_complex(a, start, end, current_health, bridges, current_monsters):
    start_x, start_y = start
    end_x, end_y = end
    
    # score_matrix[y][x] stores the highest score achieved to reach this tile
    # Initialize with negative infinity
    score_matrix = [[-float('inf') for _ in range(len(a[0]))] for _ in range(len(a))]
    parent_matrix = [[None for _ in range(len(a[0]))] for _ in range(len(a))]
    health_matrix = [[0 for _ in range(len(a[0]))] for _ in range(len(a))]

    # Priority Queue stores: (-current_score, x, y, current_hp, steps)
    # We use negative score because heapq is a min-heap
    pq = [(-0, start_x, start_y, current_health, 0)]
    score_matrix[start_y][start_x] = 0
    health_matrix[start_y][start_x] = current_health

    while pq:
        neg_score, x, y, hp, steps = heapq.heappop(pq)
        curr_score = -neg_score

        # If we reached the goal, this is the highest score path due to PQ
        if (x, y) == (end_x, end_y):
            # Backtrack to find the path
            path = []
            curr = (x, y)
            while curr:
                path.append(curr)
                curr = parent_matrix[curr[1]][curr[0]]
            return path[::-1], hp

        # Check bridge constraints
        allowed_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if (x, y) in bridges:
            orientation = bridges[(x, y)]
            allowed_dirs = [(-1, 0), (1, 0)] if orientation == "NS" else [(0, -1), (0, 1)]

        for dy, dx in allowed_dirs:
            nx, ny = x + dx, y + dy
            
            if 0 <= ny < len(a) and 0 <= nx < len(a[0]):
                is_monster = (nx, ny) in current_monsters
                if a[ny][nx] == 1 and not is_monster:
                    continue

                # Calculate damage
                damage = 0
                if is_monster:
                    m_stat = monster_stats[current_monsters[(nx, ny)]]
                    damage += m_stat["damage"] * m_stat["freq"]
                
                # Proximity damage (8-square)
                for sy in range(ny - 1, ny + 2):
                    for sx in range(nx - 1, nx + 2):
                        if (sx, sy) in current_monsters and (sx, sy) != (nx, ny):
                            damage += monster_stats[current_monsters[(sx, sy)]]["damage"]

                new_hp = hp - damage
                if new_hp <= 0: continue

                # Calculate new score for this step
                # These weights define if circumvention is better than combat
                step_penalty = step_score
                hp_weight = hp_score
                
                # Move Score = (points from health) - (points lost from steps)
                # Note: We use relative score change here
                move_score = curr_score - (damage * hp_weight) - step_penalty

                if move_score > score_matrix[ny][nx]:
                    score_matrix[ny][nx] = move_score
                    health_matrix[ny][nx] = new_hp
                    parent_matrix[ny][nx] = (x, y)
                    heapq.heappush(pq, (-move_score, nx, ny, new_hp, steps + 1))

    return None # No survivable path

def generate_maze_image(grid, path, monsters, gems, start, end, filename="solved_path.png"):
    zoom = 40  # Size of each cell in pixels
    rows = len(grid)
    cols = len(grid[0])
    
    # Create a blank RGB image
    img = Image.new("RGB", (cols * zoom, rows * zoom), "white")
    draw = ImageDraw.Draw(img)

    for y in range(rows):
        for x in range(cols):
            top_left = (x * zoom, y * zoom)
            bottom_right = ((x + 1) * zoom, (y + 1) * zoom)
            rect = [top_left, bottom_right]

            # Color coding the grid
            if grid[y][x] == 1:
                draw.rectangle(rect, fill="black") # Walls
            
            # Special Markers
            if (x, y) == start:
                draw.rectangle(rect, fill="green") # Start
            elif (x, y) == end:
                draw.rectangle(rect, fill="red")   # Exit
            elif (x, y) in gems:
                draw.ellipse([x*zoom+10, y*zoom+10, (x+1)*zoom-10, (y+1)*zoom-10], fill="blue") # Gems
            elif (x, y) in monsters:
                draw.polygon([(x*zoom+20, y*zoom+5), (x*zoom+5, y*zoom+35), (x*zoom+35, y*zoom+35)], fill="purple") # Monsters

    # Draw the Path
    if path:
        for i in range(len(path) - 1):
            p1 = path[i]
            p2 = path[i+1]
            # Draw line between centers of cells
            line_start = (p1[0] * zoom + zoom//2, p1[1] * zoom + zoom//2)
            line_end = (p2[0] * zoom + zoom//2, p2[1] * zoom + zoom//2)
            draw.line([line_start, line_end], fill="orange", width=5)

    img.save(filename)
    print(f"Maze image saved as {filename}")


# --- Main Execution ---
if __name__ == "__main__":
    # Import and correct the maze data
    original_grid = copy.deepcopy(maze_data.maze_grid)
    HEIGHT = len(original_grid)
    WIDTH = len(original_grid[0])
    
    # 2. COORDINATE TRANSFORMATION (Unity Y -> Python Row Index)
    # Unity (0,0) is bottom-left. Python [0][0] is top-left.
    # Because the grid is top-down, we only need to flip the Y value.
    def ty(y): return (HEIGHT - 1) - y

    start_pos = (maze_data.start[0], ty(maze_data.start[1]))
    end_pos = (maze_data.end[0], ty(maze_data.end[1]))
    gems = [(x, ty(y)) for x, y in maze_data.gem_positions]
    
    # Transform dictionary keys for Monsters and Bridges
    master_monster_types = {(x, ty(y)): t for (x, y), t in maze_data.monster_types.items()}
    bridges = {(x, ty(y)): o for (x, y), o in getattr(maze_data, 'bridge_data', {}).items()}



    # Run Dijkstra
    best_overall_path = []
    max_total_score = -float('inf')
    best_sequence = None

    # 2. Brute Force the Order of Gems
    gem_sequences = list(itertools.permutations(gems))
    print(f"--- Starting Dijkstra-Permutation Search ({len(gem_sequences)} sequences) ---")

    for sequence in gem_sequences:
        current_grid = copy.deepcopy(original_grid)
        current_monsters = copy.deepcopy(master_monster_types)
        current_hp = 300
        current_loc = start_pos
        current_total_path = []
        valid_sequence = True
        
        # Journey stops: Start -> Gem A -> Gem B -> Gem C -> End
        full_stops = list(sequence) + [end_pos]
        
        for next_goal in full_stops:
            # solve_dijkstra_complex returns the path with the best possible score
            result = solve_dijkstra_complex(
                current_grid, 
                current_loc, 
                next_goal, 
                current_hp, 
                bridges, 
                current_monsters
            )
            
            if result is None:
                valid_sequence = False
                break
            
            segment_path, segment_end_hp = result
            
            # Update local state: Remove monsters defeated in this segment
            for coord in segment_path:
                if coord in current_monsters:
                    current_grid[coord[1]][coord[0]] = 0 
                    current_monsters.pop(coord)
            
            # Combine paths (avoiding duplicating the stop-over point)
            if not current_total_path:
                current_total_path += segment_path
            else:
                current_total_path += segment_path[1:]
                
            current_hp = segment_end_hp
            current_loc = next_goal

        # 3. Final Scoring and Path Selection
        if valid_sequence:
            total_steps = len(current_total_path) - 1 # steps are transitions
            # Rubric Score: (Gems * 1000) + (HP * 10) - (Steps * 2)
            final_score = (len(gems) * gem_score) + (current_hp * hp_score) - (total_steps * step_score)
            
            if final_score > max_total_score:
                max_total_score = final_score
                best_overall_path = current_total_path
                best_sequence = sequence
                print(f"New Best Path Found! Order: {sequence} | Score: {final_score}")

    # 4. Final Result Output
    print("\n" + "="*50)
    print("BASELINE OPTIMAL SOLUTION")
    print("="*50)
    if best_overall_path:
        print(f"Optimal Gem Order: {best_sequence}")
        print(f"Max Score: {max_total_score}")
        print(f"Final Path ({len(best_overall_path)} coordinates):")
        print(best_overall_path)
        
        # 5. Generate Visualization
        # We pass the original grid and monsters to show the initial state
        generate_maze_image(
            original_grid, 
            best_overall_path, 
            master_monster_types, 
            gems, 
            start_pos, 
            end_pos
        )
    else:
        print("No valid path found. All character permutations resulted in death or dead-ends.")