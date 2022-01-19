from queue import PriorityQueue
from PathfindingAlgorithms.AlgorithmUtils import h, reconstruct_path


def a_star(grid, start, end, draw):
    #Count keeps track of when node is inserted into the priority queue
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    #Keep track of where node came from (path):
    came_from = {}
    
    #F = g + h
    #g = distance to start node 
    #h = distance to end node
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    #open set has keeps track of nodes that are in or not in the priority queue
    open_set_hash = {start}
        
    #While there are still nodes in the priority queue
    while not open_set.empty():
        #Index 2 is the node (0 is f_score, 1 is count)
        current = open_set.get()[2]
        open_set_hash.remove(current)
        start.make_start()
        end.make_end()
        
        #If the algorithm found a path to the end
        if current == end:
            return reconstruct_path(came_from, start, end, lambda: draw())
        
        neighbors = current.get_neighbors(grid)
        
        for neighbor in neighbors:
            if(not neighbor.is_barrier()):
                temp_g_score = g_score[current] + 1
                
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        if neighbor != start and neighbor != end:
                            neighbor.make_open()
                        
        draw()
         
        if current != start and current != end:
            current.make_closed()
        
    #Path not found    
    return None