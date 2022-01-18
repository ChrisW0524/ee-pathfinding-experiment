import random

def generate_maze(grid, grid_size, start, end):
    start = grid[1][1]
    start.make_cell()
    walls = []
    neighbors = start.get_neighbors(grid)
    for node in neighbors:
        walls.append(node)
        node.make_barrier()    
    
    end = grid[grid_size-1][grid_size-1]
    end.make_end()
    
    while walls:
        
        # for i in range(1):
        #     draw(window, grid, grid_size, WINDOW_SIZE)
        rand_wall = walls[int(random.random()*len(walls))-1]
        
        wall_top = rand_wall.get_top_neighbor(grid)
        wall_bottom = rand_wall.get_bottom_neighbor(grid)
        wall_left = rand_wall.get_left_neighbor(grid)
        wall_right = rand_wall.get_right_neighbor(grid)  
        
        #print(wall_top.get_pos(),wall_bottom.get_pos(),wall_left.get_pos(),wall_right.get_pos())  
        
        if(wall_top):
            #wall_top is unvisited and wall_bottom is cell
            if(wall_top.is_unvisited() and wall_bottom.is_cell()):
                s_cells = get_surrounding_cells(grid, rand_wall)
                if s_cells < 2:
                    rand_wall.make_cell()
                
                    #Cell on right of rand_wall
                    if(wall_right):
                        if(not wall_right.is_cell()):
                            wall_right.make_barrier()
                        if(wall_right not in walls):
                            walls.append(wall_right)
                            
                    #Cell left of rand_wall
                    if(wall_left):
                        if(not wall_left.is_cell()):
                            wall_left.make_barrier()
                        if(wall_left not in walls):
                            walls.append(wall_left)
                            
                    #Cell top of rand_wall
                    if(wall_top):
                        if(not wall_top.is_cell()):
                            wall_top.make_barrier()
                        if(wall_top not in walls):
                            walls.append(wall_top)
                    
                            
                
                walls.remove(rand_wall)
                continue
        if(wall_bottom):
            #wall_bottom is unvisited and wall_top is Cell
            if(wall_bottom.is_unvisited() and wall_top.is_cell()):
                s_cells = get_surrounding_cells(grid, rand_wall)
                if s_cells < 2:
                    rand_wall.make_cell()
                
                    #Cell on right of rand_wall
                    if(wall_right):
                        if(not wall_right.is_cell()):
                            wall_right.make_barrier()
                        if(wall_right not in walls):
                            walls.append(wall_right)
                            
                    #Cell left of rand_wall
                    if(wall_left):
                        if(not wall_left.is_cell()):
                            wall_left.make_barrier()
                        if(wall_left not in walls):
                            walls.append(wall_left)
                            
                    #Cell on bottom of rand_wall
                    if(wall_bottom):
                        if(not wall_bottom.is_cell()):
                            wall_bottom.make_barrier()
                        if(wall_bottom not in walls):
                            walls.append(wall_bottom)
                        
                walls.remove(rand_wall)
                continue
        if(wall_left):
            #wall_left is unvisited and wall_right is Cell
            if(wall_left.is_unvisited() and wall_right.is_cell()):
                s_cells = get_surrounding_cells(grid, rand_wall)
                if s_cells < 2:
                    rand_wall.make_cell()
                    
                    #Cell top of rand_wall
                    if(wall_top):
                        if(not wall_top.is_cell()):
                            wall_top.make_barrier()
                        if(wall_top not in walls):
                            walls.append(wall_top)
                            
                    #Cell on bottom of rand_wall
                    if(wall_bottom):
                        if(not wall_bottom.is_cell()):
                            wall_bottom.make_barrier()
                        if(wall_bottom not in walls):
                            walls.append(wall_bottom)
                            
                    #Cell left of rand_wall
                    if(wall_left):
                        if(not wall_left.is_cell()):
                            wall_left.make_barrier()
                        if(wall_left not in walls):
                            walls.append(wall_left)
            
                walls.remove(rand_wall)
                continue
        if(wall_right):
            #wall_right is unvisited and wall_left is Cell
            if(wall_right.is_unvisited() and wall_left.is_cell()):
                s_cells = get_surrounding_cells(grid, rand_wall)
                if s_cells < 2:
                    rand_wall.make_cell()
                    
                    #Cell top of rand_wall
                    if(wall_top):
                        if(not wall_top.is_cell()):
                            wall_top.make_barrier()
                        if(wall_top not in walls):
                            walls.append(wall_top)
                            
                    #Cell on bottom of rand_wall
                    if(wall_bottom):
                        if(not wall_bottom.is_cell()):
                            wall_bottom.make_barrier()
                        if(wall_bottom not in walls):
                            walls.append(wall_bottom)
                            
                    #Cell on right of rand_wall
                    if(wall_right):
                        if(not wall_right.is_cell()):
                            wall_right.make_barrier()
                        if(wall_right not in walls):
                            walls.append(wall_right)
                
                walls.remove(rand_wall)
                continue
            
        
        
        walls.remove(rand_wall)  
        continue  
    
    #Entrance
    grid[0][1].make_cell()
    grid[1][0].make_cell()
    grid[1][1].make_cell()
    #Exit
    grid[grid_size-1][grid_size-2].make_cell()
    grid[grid_size-2][grid_size-1].make_cell()
    grid[grid_size-2][grid_size-2].make_cell()
    
    start.make_cell()
    start = grid[0][0]
    start.make_start()
    
    for row in grid:
        for node in row:
            if(node.is_unvisited()):
                node.make_barrier()
                
    for row in grid:
        for node in row:
            if(node.is_cell()):
                node.reset()        
                
    
    start.make_start()
    
def get_surrounding_cells(grid, rand_wall):
    s_cells = 0
    #If top wall is cell
    if(rand_wall.get_top_neighbor(grid)):
        if(rand_wall.get_top_neighbor(grid).is_cell()):
            s_cells += 1
    
    #If bottom wall is cell
    if(rand_wall.get_bottom_neighbor(grid)):
        if(rand_wall.get_bottom_neighbor(grid).is_cell()):
            s_cells += 1
        
    #If left wall is cell
    if(rand_wall.get_left_neighbor(grid)):
        if(rand_wall.get_left_neighbor(grid).is_cell()):
            s_cells += 1
        
    #If right wall is cell
    if(rand_wall.get_right_neighbor(grid)):
        if(rand_wall.get_right_neighbor(grid).is_cell()):
            s_cells += 1
        
    return s_cells