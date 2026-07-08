def mine_sweeper(grid):
    # Determine the grid boundaries
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    # Create a deep copy of the grid to build our results
    result = [row[:] for row in grid]

    # Relative coordinate offsets for all 8 neighboring directions
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    # Iterate through each cell in the 2D grid using nested enumerate
    for r_idx, row in enumerate(grid):
        for c_idx, cell in enumerate(row):
            # If the cell contains a mine, leave it unchanged
            if cell == "#":
                continue

            # Count adjacent mines
            mine_count = 0
            for dr, dc in directions:
                neighbor_row = r_idx + dr
                neighbor_col = c_idx + dc
            # Confirm neighbor cell falls safely inside bounds
            if 0 <= neighbor_row < num_rows and 0 <= neighbor_col < num_cols:
                    if grid[neighbor_row][neighbor_col] == "#":   
                     mine_count += 1

            result[r_idx][c_idx] = mine_count

    return result

# Define a function to print the grid in a formatted manner
def print_grid(input_grid):
    if not input_grid:
        print("Invalid grid: Empty")
        return
    # Print the grid
    print("[", end="")
    for i in range(len(input_grid)):
        print("", input_grid[i], end="")
        if i != len(input_grid) - 1:
            print(",")
        else:
            print(end="")
            print(" ]") 


# A grid for testing
if __name__ == "__main__":
    input_grid = [
        ["-","-","-","#","#"],
        ["-","#","-","-","-"],
        ["-","-","#","-","-"],
        ["-","#","#","-","-"],
        ["-","-","-","-","-"]
    ]

    output_grid  = mine_sweeper(input_grid)

    print("Minesweeper Output Grind:")
    for row in output_grid:
        print(row)