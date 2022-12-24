# Day 24. Blizzard Basin 
# https://adventofcode.com/2022/day/24

from copy import deepcopy
from collections import deque
from util.input_util import read_input_file

WALL = '#'
SPACE = '.'

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'

DIRMAP = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}

ALLDIRS = { (0, 0), (1, 0), (-1, 0), (0, 1), (0, -1) }

def parse_lines():
    lines = read_input_file(24)
    grid = []
    blizzards = []
    
    for l in lines:
        grid.append(list(l))
    
    NROWS = len(grid)
    NCOLS = len(grid[0])
    for r in range(NROWS):
        for c in range(NCOLS):
            if r == 0 and grid[r][c] == SPACE: 
                START = (r, c)

            elif r == NROWS-1 and grid[r][c] == SPACE:
                END = (r, c)

            elif grid[r][c] in (UP, DOWN, LEFT, RIGHT):
                # Track blizzard location and direction
                blizzards.append((r, c, grid[r][c]))
                grid[r][c] = SPACE
    
    return grid, START, END, NROWS, NCOLS, blizzards
    

def print_grid(grid, blizzards, loc):
    grid = deepcopy(grid)
    for r, c, d in blizzards:
        grid[r][c] = d
    
    grid[loc[0]][loc[1]] = 'E'

    s = ''
    for g in grid:
        s += ''.join(g) + '\n'
    print(s)
    return s


def move_blizzard(grid, blizzard, NROWS, NCOLS):
    r, c, d = blizzard
    dr, dc = DIRMAP[d]
    while True:
        r = (r + dr) % NROWS 
        c = (c + dc) % NCOLS
        if grid[r][c] != WALL:
            return r, c, d
    

def move_all_blizzards(grid, blizzards, NROWS, NCOLS):
    
    blizzardlocations = set()
    for i, b in enumerate(blizzards):
        r, c, d = move_blizzard(grid, b, NROWS, NCOLS)
        blizzards[i] = (r, c, d)
        blizzardlocations.add((r, c))
    return blizzardlocations


# Detect cycles in blizzards
def blizzard_states(grid, START, END, NROWS, NCOLS, blizzards):
    seen = set()
    state = {}
    
    i = 0
    while True:
        t = tupbliz = tuple(blizzards)
        if t in seen:
            return state
        
        seen.add(t)
        state[i] = tuple((r, c) for r ,c, _ in blizzards)
        move_all_blizzards(grid, blizzards, NROWS, NCOLS)
        i += 1
        
        

def travel(grid, START, END, min, states, NROWS, NCOLS):
    seen = set()
    q = deque([(START, min)])
    
    while q:
        print(f'Queue length: {len(q)}\r', end='')
        loc, mins = q.popleft()
        if loc == END:
            return mins

        if (loc, mins) in seen:
            continue
        seen.add((loc, mins))
        
        r, c = loc
        nm = mins + 1
        bliz = states[nm % len(states)]
        for dr, dc in ALLDIRS:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < NROWS and 0 <= nc < NCOLS:
                if grid[nr][nc] != WALL and (nr, nc) not in bliz:
                    if ((nr, nc), nm) not in seen:
                        q.append( ((nr, nc), nm) )
                    
    raise ValueError("No path found")
             
                    
        
def solution1():
    grid, START, END, NROWS, NCOLS, blizzards = parse_lines()
    states = blizzard_states(grid, START, END, NROWS, NCOLS, deepcopy(blizzards))

    # Travel to End    
    min1 = travel(grid, START, END, 0, states, NROWS, NCOLS)
    print()
    print('Start to End:', min1)

    return min1


def solution2():
    grid, START, END, NROWS, NCOLS, blizzards = parse_lines()
    states = blizzard_states(grid, START, END, NROWS, NCOLS, deepcopy(blizzards))

    # Travel to End
    min1 = travel(grid, START, END, 0, states, NROWS, NCOLS)
    print()
    print('Start to End:', min1)
    
    # Travel back to Start
    min2 = travel(grid, END, START, min1, states, NROWS, NCOLS)
    print()
    print('End to Start:', min2)
    
    # Travel back to End
    min3 = travel(grid, START, END, min2, states, NROWS, NCOLS)
    print()
    print('Start to End:', min3)

    print(min1, min2, min3)
    
    return min3  
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
