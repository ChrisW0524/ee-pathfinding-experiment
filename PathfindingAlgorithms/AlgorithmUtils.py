from importlib.resources import path


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2)+abs(y1 - y2)

def reconstruct_path(came_from, start, current, draw):
    
    path_length = 0
    
    while current in came_from: 
        current = came_from[current]
        if(current != start):
            path_length+= 1 
            current.make_path()
        draw()
    
    return path_length
