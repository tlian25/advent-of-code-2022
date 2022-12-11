# Day 9. Rope Bridge 
# https://adventofcode.com/2022/day/9


import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from PIL import Image
from util.input_util import read_input_file

dir_map = {'L': (-1, 0), 'R': (1, 0), 'U': (0, 1), 'D': (0, -1)}

def parse_line(l:str) -> tuple:
    d, s = l.split(' ')
    steps = int(s)
    dir = dir_map[d]
    return dir, steps


def get_moves():
    lines = read_input_file(9)
    moves = []
    for l in lines:
        dir, steps = parse_line(l)
        for _ in range(steps):
            moves.append(dir)
    
    return moves
        

def get_dist(H:tuple, T:tuple) -> float:
    return ((H[0] - T[0]) ** 2 + (H[1] - T[1]) ** 2) ** 0.5


def get_head_positions() -> list:
    H = (0, 0)
    positions = [H]
    
    moves = get_moves()
    for m in moves:
        newH = (H[0] + m[0], H[1] + m[1])
        H = newH
        positions.append(H)
        
    return positions


def get_closest_move(H, T) -> list:
    if get_dist(H, T) < 1.5:
        return T
    
    # brute force best move around H
    dirs = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
    dist = 100
    best_move = None
    for x, y in dirs:
        newT = T[0] + x, T[1] + y
        d = get_dist(H, newT)
        if d < dist:
            best_move = newT
            dist = d
            
    return best_move
    


def print_grid(visited:set):
    xs = [v[0] for v in visited]
    ys = [v[1] for v in visited]
    
    minx = min(xs)
    maxx = max(xs)
    miny = min(ys)
    maxy = max(ys)
    
    s = ''
    for y in range(maxy, miny-1, -1):
        for x in range(minx, maxx+1):
            if (x, y) in visited:
                s += '#'
            else:
                s += '.'
        s += '\n'
        
    print(s)
    


# For each Head position, get the best possible tail position
def get_tail_positions(positions) -> list:
    T = (0, 0)
    visited = [T]
    for i in range(1, len(positions)):
        T = get_closest_move(positions[i], T)
        visited.append(T)
            
    return visited


def solution1():
    # H and T must always be touching
    # Diagonal and overalapping both count as touching
    # Count all of the positions the tail visited at least once
  
    head_positions = get_head_positions()
    visited = get_tail_positions(head_positions)
            
    uniq_visited = set(visited)
    return len(uniq_visited)
            


def solution2():
    positions = get_head_positions()
    for i in range(1, 10):
        positions = get_tail_positions(positions)
    
    uniq_visited = set(positions)
    return len(uniq_visited)



#### Some extra code to create a mini movie of rope movements
    
def solution2_to_images():

    head_positions = get_head_positions()
    positions = [head_positions]

    
    for i in range(1, 10):
        positions.append(get_tail_positions(positions[i-1]))
        
    xs = [abs(p[0]) for p in head_positions]
    ys = [abs(p[1]) for p in head_positions]
    
    S = max(max(xs), max(ys))
    
    tail_visited = set()
    
    WIDTH = 640
    HEIGHT = 480
    
    frame = 0
    for step in range(0, len(head_positions), 10):
        if step % 100 == 0:
            print(step)
        
        # PLT method
        fig, ax = plt.subplots()
        ax.set_xlim([-S, S])
        ax.set_ylim([-S, S])
        for knot in range(len(positions)):
            color = (0, 0, (15-knot) / 20)
            ax.add_patch(Rectangle(positions[knot][step], 5, 5, color = color))
            
        
        for t in tail_visited:
            ax.add_patch(Circle(t, 2, color = 'green'))
        
        tail_visited.add(positions[-1][step])
        
        plt.savefig(f'images/image_{str(frame).zfill(8)}.png')
        plt.close()
        frame += 1
        

        
            
            
    

                
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
    
    #solution2_to_images()
