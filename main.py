import pygame
import sys
import math
import random

#Pygame setup
WINDOW_SIZE = 1000
pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE));
pygame.display.set_caption("Pathfinding EE experiment")
pygame.display.update();

#Colors
RED = (255, 0, 0) # Closed node
GREEN = (0, 255, 0) # Open node
BLUE = (0, 255, 0) 
YELLOW = (255, 255, 0) # Cell
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) # Barrier node
PURPLE = (128, 0, 128) # Path node
ORANGE = (255, 165 ,0) # Start node
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208) #End node    

#node class
class Node:
    def __init__(self, col, row, size, total_rows):
        self.col = col
        self.row = row
        self.x = col * size
        self.y = row * size
        self.color = WHITE
        self.neighbors = []
        self.size = size
        self.total_rows = total_rows
        
    #Col = X coordinate
    #Row = Y coordinate
    #returns (y, x)    
    def get_pos(self):
        return self.col, self.row
    
    def is_unvisited(self):
        return self.color == WHITE
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_cell(self):
        return self.color == YELLOW
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
        
    def make_cell(self):
        self.color = YELLOW
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE
    
    def make_end(self):
        self.color = TURQUOISE
        
    def make_path(self):
        self.color = PURPLE
    
    def reset(self):
        self.color = WHITE
        
    def get_left_neighbor(self, grid):
        if(self.col-1>=0):
            return grid[self.col-1][self.row]
        
    def get_right_neighbor(self, grid):
        if(self.col+1<=len(grid)-1):
            return grid[self.col+1][self.row]
        
    def get_top_neighbor(self, grid):
        if(self.row-1>=0):
            return grid[self.col][self.row-1]
        
    def get_bottom_neighbor(self, grid):
        if(self.row+1<=len(grid)-1):
            return grid[self.col][self.row+1]  
            
    def get_neighbors(self, grid):
        neighbors = []
        #Left neighbor
        if(self.col-1>=0):
            neighbors.append(grid[self.col-1][self.row])
        #Right neighbor
        if(self.col+1<=len(grid)-1):
            neighbors.append(grid[self.col+1][self.row])
        #Top neighbor
        if(self.row-1>=0):
            neighbors.append(grid[self.col][self.row-1])
        #Bottom neighbor
        if(self.row+1<=len(grid)-1):
            neighbors.append(grid[self.col][self.row+1])    
        
        return neighbors
        
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))
        
def make_grid(grid_size, window_size):
    grid = []
    gap = window_size // grid_size
    for i in range(grid_size):
        grid.append([])
        for j in range(grid_size):
            node = Node(i, j, gap, grid_size)
            grid[i].append(node)
            
    return grid

def draw_grid_lines(window, grid_size, window_size):
    gap = window_size // grid_size
    for i in range(grid_size):
        pygame.draw.line(window, GREY, (0, i * gap), (window_size, i * gap))
        for j in range(grid_size):
            pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, window_size))
    pass
    
def draw(window, grid, grid_size, window_size):
    window.fill(WHITE)
    
    for row in grid:
        for spot in row:
            spot.draw(window)
            
    draw_grid_lines(window, grid_size, window_size)
    pygame.display.update()
    
def randomize_grid(grid, density, start, end):
    grid_size = len(grid)
    
    for row in grid:
        for node in row:
            node.reset()
            if(random.random() < density):
                node.make_barrier()
                
    grid[0][0].make_start()
    grid[grid_size - 1][grid_size - 1].make_end()
            
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
    
    make_entrance_exit(grid, grid_size)
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
                
    
    print("Generation completed!")
    start.make_start()
    
def make_entrance_exit(grid, grid_size):
    #Entrance
    grid[0][1].make_cell()
    grid[1][0].make_cell()
    grid[1][1].make_cell()
    #Exit
    grid[grid_size-1][grid_size-2].make_cell()
    grid[grid_size-2][grid_size-1].make_cell()
    grid[grid_size-2][grid_size-2].make_cell()
    
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	x, y = pos

	row = y // gap
	col = x // gap

	return col, row

def main(window, window_size):
    ROWS = 25
    grid = make_grid(ROWS, window_size)
    
    start = None
    end = None
    
    run = True
    started = False
    
    while run:
        draw(window, grid, ROWS, window_size)
        for event in pygame.event.get():
            # if pygame.mouse.get_pressed()[0]:
            #     pos = pygame.mouse.get_pos()
            #     col, row = get_clicked_pos(pos, ROWS, WINDOW_SIZE)
            #     node = grid[col][row]
            #     print(node.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    randomize_grid(grid, 0.25, start, end)
                if event.key == pygame.K_z:
                    for row in grid:
                        for node in row:
                            node.reset()
                    generate_maze(grid, ROWS, start, end)

            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
    pygame.quit()
    
main(window, WINDOW_SIZE)