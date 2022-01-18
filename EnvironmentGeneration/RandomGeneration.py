import random

def randomize_grid(grid, density, start, end):
    grid_size = len(grid)
    
    for row in grid:
        for node in row:
            node.reset()
            if(random.random() < density):
                node.make_barrier()
                
    start = grid[0][0]
    start.make_start()
    end = grid[grid_size - 1][grid_size - 1]
    end.make_end()