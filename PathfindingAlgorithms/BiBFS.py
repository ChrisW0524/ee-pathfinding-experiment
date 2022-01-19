from queue import PriorityQueue
from PathfindingAlgorithms.AlgorithmUtils import reconstruct_path

def bi_bfs(grid, start, end, draw):
    count = 0
    open_set = PriorityQueue()
    open_set.put((count, start))
    
    #Keep track of where node came from (path):
    came_from = {}
    
    while not open_set.empty():
        current = open_set.get()[1]
        
        #If the algorithm found a path to the end
        if current == end:
            came_from.pop(start)
            return reconstruct_path(came_from, start, end, lambda: draw())

        
        neighbors = current.get_neighbors(grid)
        
        for neighbor in neighbors:
            if(not neighbor.is_barrier()):
                if neighbor not in came_from:
                    count += 1
                    open_set.put((count, neighbor))
                    came_from[neighbor] = current
                    if neighbor != start and neighbor != end:
                                neighbor.make_open()
                                
        draw()
        if current != start and current != end:
            current.make_closed()
            
    #Path not found
    return None