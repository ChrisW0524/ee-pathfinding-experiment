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
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) # Barrier node
PURPLE = (128, 0, 128) # Path node
ORANGE = (255, 165 ,0) # Start node
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208) #End node    

#node class
class Node:
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.color = WHITE
        self.neighbors = []
        self.size = size
        self.total_rows = total_rows
        
    #Row = Y coordinate
    #Col = X coordinate
    #returns (y, x)    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
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
    
def randomize_grid(grid, density):
    for row in grid:
        for node in row:
            node.reset()
            if(random.random() < density):
                node.make_barrier()
            

def main(window, window_size):
    ROWS = 100
    grid = make_grid(ROWS, window_size)
    
    start = None
    end = None
    
    run = True
    started = False

    while run:
        draw(window, grid, ROWS, window_size)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    randomize_grid(grid, 0.25)

            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
    pygame.quit()
    
main(window, WINDOW_SIZE)