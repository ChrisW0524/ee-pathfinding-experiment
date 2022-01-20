from re import A
import pygame
import csv
from time import perf_counter


#import algorithms
from EnvironmentGeneration.MazeGeneration import generate_maze
from EnvironmentGeneration.RandomGeneration import randomize_grid
from PathfindingAlgorithms.Astar import a_star
from PathfindingAlgorithms.GreedyBFS import greedy_bfs
from PathfindingAlgorithms.BiBFS import bi_bfs


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

row_size = 10
is_maze = False

DRAW_ANIMATION = False
RANDOM_DENSITY = 0.25

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
        
    def __str__(self):
        pos = self.get_pos()
        return str(pos)       
def make_grid(grid_size, window_size):
    grid = []
    gap = window_size // grid_size
    for i in range(grid_size):
        grid.append([])
        for j in range(grid_size):
            node = Node(i, j, gap, grid_size)
            grid[i].append(node)
            
    start = grid[0][0]
    start.make_start()
    end = grid[row_size - 1][row_size - 1]
    end.make_end()
            
    return (grid, start, end)
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
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	x, y = pos

	row = y // gap
	col = x // gap

	return col, row
def reset_grid_colors(grid, start, end):
    for row in grid:
        for node in row:
            if(node != start and node != end and not node.is_barrier()):
                node.reset()                
def run_algorithm(grid, start, end, algorithm):
    reset_grid_colors(grid,start,end)
    path_length = None
    while path_length is None:   
        t_start = perf_counter()    
        
        if algorithm == "a_star":             
            path_length = a_star(grid, start, end, lambda: draw(window, grid, row_size, WINDOW_SIZE)) if DRAW_ANIMATION else a_star(grid, start, end, lambda: None)
        if algorithm == "greedy_bfs":
            path_length = greedy_bfs(grid, start, end, lambda: draw(window, grid, row_size, WINDOW_SIZE)) if DRAW_ANIMATION else greedy_bfs(grid, start, end, lambda: None)
        if algorithm == "bi_bfs":
            path_length = bi_bfs(grid, start, end, lambda: draw(window, grid, row_size, WINDOW_SIZE)) if DRAW_ANIMATION else bi_bfs(grid, start, end, lambda: None)
        
        if(path_length is None):
            if(is_maze):
                generate_maze(grid, row_size, start, end)
            else:
                randomize_grid(grid, RANDOM_DENSITY, start, end)
                
        t_stop = perf_counter()
    
    return (t_stop - t_start, path_length)
def collect_data():
    global row_size
    MIN_GRID_SIZE = 10
    MAX_GRID_SIZE = 50
    GRID_ITERATIONS = 10
    ALGORITHM_ITERATIONS = 10
    
    #Random environment
    f = open("random_grid.csv", "w+", newline="")
    f.truncate()
    writer = csv.writer(f)
    column_header = ("Grid size","A* Average time", "A* Path Length", "Greedy BFS Average time", "Greedy BFS Path Length", "Bi-BFS Average time", "Bi-BFS Path Length")
    writer.writerow(column_header)
        
    #Loop through different grid sizes
    for grid_size in range(MIN_GRID_SIZE, MAX_GRID_SIZE):
        row_size = grid_size
        grid, start, end = make_grid(row_size, WINDOW_SIZE)
        
        #loop through each grid size for some iterations
        for i in range(GRID_ITERATIONS):
            randomize_grid(grid, RANDOM_DENSITY, start, end)
            path_length_data = [0, 0, 0]
            time_data = [[],[],[]]
            
            #For each grid run each algorithm for x times and calculate their average time
            for j in range(ALGORITHM_ITERATIONS):
                result = run_algorithm(grid, start, end, "a_star")
                time_data[0].append(result[0]) 
                path_length_data[0] = result[1] 
                
                result = run_algorithm(grid, start, end, "greedy_bfs")
                time_data[1].append(result[0])  
                path_length_data[1] = result[1]
                
                result = run_algorithm(grid, start, end, "bi_bfs")
                time_data[2].append(result[0])  
                path_length_data[2] = result[1]
                
            writer.writerow((grid_size, path_length_data[0], sum(time_data[0])/len(time_data[0]), path_length_data[1], sum(time_data[1])/len(time_data[1]), path_length_data[2], sum(time_data[2])/len(time_data[2])))
    f.close()
    
    #Generated mazes
    f = open("generated_maze.csv", "w+", newline="")
    f.truncate()
    writer = csv.writer(f)
    column_header = ("Grid size","A* Average time", "A* Path Length", "Greedy BFS Average time", "Greedy BFS Path Length", "Bi-BFS Average time", "Bi-BFS Path Length")
    writer.writerow(column_header)
    
    # Loop through different grid sizes
    for grid_size in range(MIN_GRID_SIZE, MAX_GRID_SIZE):
        row_size = grid_size
        grid, start, end = make_grid(row_size, WINDOW_SIZE)
        
        #loop through each grid size for some iterations
        for i in range(GRID_ITERATIONS):
            generate_maze(grid, row_size, start, end)
            path_length_data = [0, 0, 0]
            time_data = [[],[],[]]
            
            #For each grid run each algorithm for x times and calculate their average time
            for j in range(ALGORITHM_ITERATIONS):
                result = run_algorithm(grid, start, end, "a_star")
                time_data[0].append(result[0]) 
                path_length_data[0] = result[1] 
                
                result = run_algorithm(grid, start, end, "greedy_bfs")
                time_data[1].append(result[0])  
                path_length_data[1] = result[1]
                
                result = run_algorithm(grid, start, end, "bi_bfs")
                time_data[2].append(result[0])  
                path_length_data[2] = result[1]
                
            writer.writerow((grid_size, path_length_data[0], sum(time_data[0])/len(time_data[0]), path_length_data[1], sum(time_data[1])/len(time_data[1]), path_length_data[2], sum(time_data[2])/len(time_data[2])))
    f.close()
    
def main(window, window_size):
    global row_size
    grid, start, end = make_grid(row_size, window_size)
    run = True
    started = False
    
    while run:
        draw(window, grid, row_size, window_size)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    randomize_grid(grid, RANDOM_DENSITY, start, end)
                    is_maze = False
                if event.key == pygame.K_z:
                    generate_maze(grid, row_size, start, end)
                    is_maze = True
                if event.key == pygame.K_x:
                    result = run_algorithm(grid, start, end, "a_star")
                    print("Time elapsed: " + str(result[0]))
                    print("Path length: " + str(result[1]))
                    
                if event.key == pygame.K_c:
                    result = run_algorithm(grid, start, end, "greedy_bfs")
                    print("Time elapsed: " + str(result[0]))
                    print("Path length: " + str(result[1]))
                    
                if event.key == pygame.K_v:
                    result = run_algorithm(grid, start, end, "bi_bfs")
                    print("Time elapsed: " + str(result[0]))
                    print("Path length: " + str(result[1]))
                    
                if event.key == pygame.K_1:
                    collect_data()
                    grid, start, end = make_grid(row_size, window_size)
                    
                if event.key == pygame.K_2:
                    row_size+=1
                    grid, start, end = make_grid(row_size, window_size)


            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
    pygame.quit()
    
main(window, WINDOW_SIZE)