# Maze Data - Generated from MazeMate (Unity WebGL)
# Dimensions: 10 x 10

# Grid representation (0 = path/walkable, 1 = wall/obstacle)
maze_grid = [
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 2, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 2, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Starting position (x, y)
start = (4, 4)

# End/Goal position (x, y)
end = (9, 9)

# Initial facing direction (N=North, S=South, E=East, W=West)
initial_direction = "S"

# Gem/Collectible positions (3 found)
gem_positions = [(8, 1), (1, 1), (1, 8)]

# Heart/Health positions (0 found) - collect to defeat monsters
heart_positions = []

# Monster/Enemy positions (5 found)
monster_positions = [(4, 2), (0, 6), (8, 3), (3, 2), (2, 3)]

# Monster types for reference
monster_types = {
    (4, 2): "Bat",
    (0, 6): "Golem",
    (8, 3): "Golem",
    (3, 2): "Cactus",
    (2, 3): "Plant"
}

bridge_data = {
    (4, 3): "NS",
    (4, 5): "NS"
}