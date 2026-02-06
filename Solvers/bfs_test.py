"""
Source code modified from:
How to Solve a Maze using BFS in Python by Timur Bakibayev:
https://levelup.gitconnected.com/solve-a-maze-with-python-e9f0580979a1
"""

from PIL import Image, ImageDraw
import maze_data_generated_mazemate as maze_data
import itertools


# Character stats
initial_health = 300
enemy_damage = {"Ghost": 20, "Zombie": 40}  # Map names from maze_data.monster_types
reward_points = {"gem": 100, "heart": 50, "enemy": 30}
step_penalty = -1

def evaluate_mission(order, grid, start, end, enemies):
    current_pos = start
    total_path = [start]
    total_score = 0
    current_health = initial_health
    
    for target in order:
        # Step 1: Use BFS to get to the next objective
        segment = solve_bfs(grid, current_pos, target)
        if not segment: return -float('inf'), [] # Unreachable
        
        # Step 2: Calculate Score/Health
        total_score += (len(segment) - 1) * step_penalty
        
        # Check if we hit an enemy during this segment
        # In a real brute force, you'd check every step in 'segment'
        for step in segment:
            if step in enemies:
                enemy_type = maze_data.monster_types.get(step, "Ghost")
                current_health -= enemy_damage.get(enemy_type, 10)
                total_score += reward_points["enemy"]

        # Add reward points for reaching the target
        if target in maze_data.gem_positions: total_score += reward_points["gem"]
        elif target in maze_data.heart_positions: 
            total_score += reward_points["heart"]
            current_health = min(100, current_health + 20) # Example healing logic

        if current_health <= 0: return -float('inf'), [] # Character died
        
        total_path += segment[1:]
        current_pos = target

    # Final leg to the exit
    to_end = solve_bfs(grid, current_pos, end)
    if not to_end: return -float('inf'), []
    
    total_score += (len(to_end) - 1) * step_penalty
    total_path += to_end[1:]
    
    return total_score, total_path


images = []
zoom = 20
borders = 6

def solve_bfs(a, start, end):
    """
    Solves the maze 'a' from 'start' to 'end' using BFS.
    start and end are (x, y) tuples corresponding to (column, row).
    Returns the path as a list of coordinates (x, y).
    """
    start_x, start_y = start
    end_x, end_y = end
    
    # Check if start or end are walls
    if a[start_y][start_x] == 1 or a[end_y][end_x] == 1:
        print(f"Error: Start {start} or End {end} is inside a wall.")
        return []

    m = []
    for i in range(len(a)):
        m.append([])
        for j in range(len(a[i])):
            m[-1].append(0)
    
    # m[row][col] represents distance/visited
    m[start_y][start_x] = 1

    def make_step(k):
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == k:
                    # Directions: Up, Left, Down, Right
                    # i is row (y), j is col (x)
                    if i > 0 and m[i - 1][j] == 0 and a[i - 1][j] == 0:
                        m[i - 1][j] = k + 1
                    if j > 0 and m[i][j - 1] == 0 and a[i][j - 1] == 0:
                        m[i][j - 1] = k + 1
                    if i < len(m) - 1 and m[i + 1][j] == 0 and a[i + 1][j] == 0:
                        m[i + 1][j] = k + 1
                    if j < len(m[i]) - 1 and m[i][j + 1] == 0 and a[i][j + 1] == 0:
                        m[i][j + 1] = k + 1

    def draw_matrix(the_path=[]):
        im = Image.new('RGB', (zoom * len(a[0]), zoom * len(a)), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        for i in range(len(a)):
            for j in range(len(a[i])):
                color = (255, 255, 255)
                r = 0
                if a[i][j] == 1:
                    color = (0, 0, 0)
                if i == start_y and j == start_x:
                    color = (0, 255, 0)
                    r = borders
                if i == end_y and j == end_x:
                    color = (0, 255, 0)
                    r = borders
                draw.rectangle((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1), fill=color)
                if m[i][j] > 0:
                    r = borders
                    draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                                 fill=(255, 0, 0))
        for u in range(len(the_path) - 1):
            # Path coordinates are (x, y) -> (col, row)
            # x is index 0 of tuple, y is index 1
            x = the_path[u][0] * zoom + int(zoom / 2)
            y = the_path[u][1] * zoom + int(zoom / 2)
            x1 = the_path[u + 1][0] * zoom + int(zoom / 2)
            y1 = the_path[u + 1][1] * zoom + int(zoom / 2)
            draw.line((x, y, x1, y1), fill=(255, 0, 0), width=5)
        draw.rectangle((0, 0, zoom * len(a[0]), zoom * len(a)), outline=(0, 255, 0), width=2)
        images.append(im)

    k = 0
    # BFS Expansion
    while m[end_y][end_x] == 0:
        k += 1
        make_step(k)
        draw_matrix()
        
        # Safety break if unreachable
        if k > len(a) * len(a[0]): 
            print("Target unreachable from Start.")
            return []

    # Backtracking to find path
    # i is row (y), j is col (x)
    i, j = end_y, end_x
    k = m[i][j]
    # Path stored as (x, y)
    the_path = [(j, i)] 
    while k > 1:
        if i > 0 and m[i - 1][j] == k - 1:
            i, j = i - 1, j
            the_path.append((j, i))
            k -= 1
        elif j > 0 and m[i][j - 1] == k - 1:
            i, j = i, j - 1
            the_path.append((j, i))
            k -= 1
        elif i < len(m) - 1 and m[i + 1][j] == k - 1:
            i, j = i + 1, j
            the_path.append((j, i))
            k -= 1
        elif j < len(m[i]) - 1 and m[i][j + 1] == k - 1:
            i, j = i, j + 1
            the_path.append((j, i))
            k -= 1
        draw_matrix(the_path)

    for _ in range(10): # Hold final frame
        draw_matrix(the_path)
    
    # Return path reversed (Start -> End)
    return the_path[::-1]

# --- Main Execution ---

if __name__ == "__main__":
    # 1. Setup Data
    maze_grid = maze_data.maze_grid
    start_pos = maze_data.start
    end_pos = maze_data.end
    
    # heart_positions = maze_data.heart_positions
    gem_positions = maze_data.gem_positions
    
    # --- Run Brute Force ---
    objectives = maze_data.gem_positions + maze_data.heart_positions
    best_score = -float('inf')
    best_path = []

    for order in itertools.permutations(objectives):
        # Constraint: All gems must be in the order (can filter here)
        if not all(gem in order for gem in maze_data.gem_positions):
            continue
            
        score, path = evaluate_mission(order, maze_grid, start_pos, end_pos, maze_data.monster_positions)
        if score > best_score:
            best_score = score
            best_path = path

    print(f"Optimal Strategy Score: {best_score}") # this is better than the provided template, as it visits all the gems instead of just one
    print(f"Best Path found: {best_path}")

    # ==========================================
    # SCENARIO 1: Direct Path (Start -> Goal)
    # ==========================================
    print(f"Solving Maze directly from {start_pos} to {end_pos}...")
    
    # images = [] # Reset images
    path = solve_bfs(maze_grid, start_pos, end_pos)
    print("Direct Path found:", path)
    
    if images:
        images[0].save('maze_sols/test.gif', save_all=True, append_images=images[len(path):], optimize=False, duration=50, loop=0)
        print("Direct animation saved to 'maze_sols/default_bfs_sol.gif'")

        final_frame = images[-1]
    
        # Save it as a static PNG or JPG
        final_frame.save('maze_sols/completed_path.png')
        print("Static image of the completed path saved to 'maze_sols/completed_path.png'")

    # ==========================================
    # SCENARIO 2: With Intermediate Goal (Start -> Gem -> Goal)
    # ==========================================
    print("\n--- Challenge Scenario: Visiting a Gem first ---")
    
    if len(gem_positions) > 0:
        target_gem = gem_positions[0]
        print(f"Attempting to visit Gem at {target_gem} first...")
        
        # Reset images for the new animation so it doesn't include the previous run
        # images = [] 
        
        # Step 1: Start -> Gem
        print("  Segment 1: Start -> Gem")
        path_to_gem = solve_bfs(maze_grid, start_pos, target_gem)
        
        if path_to_gem:
            # Step 2: Gem -> End
            print("  Segment 2: Gem -> Goal")
            path_to_end = solve_bfs(maze_grid, target_gem, end_pos)
            
            if path_to_end:
                # Step 3: Combine
                # path_to_end[1:] skips the duplicate Gem position
                full_path = path_to_gem + path_to_end[1:] 
                print("Full Path via Gem:", full_path)
                
                # Save the combined animation
                if images:
                    images[0].save('maze_sols/heart_test.gif', save_all=True, append_images=images[1:], optimize=False, duration=50, loop=0)
                    print("Gem-visiting animation saved to 'maze_sols/heart_bfs_sol.gif'")
            else:
                print("Could not reach Goal from Gem.")
        else:
            print("Could not reach Gem from Start.")
    else:
        print("No gems defined in maze_data!")
