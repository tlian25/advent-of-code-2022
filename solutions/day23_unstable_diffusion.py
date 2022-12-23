# Day 23. Unstable Diffusion
# https://adventofcode.com/2022/day/23

from collections import deque, defaultdict
from util.input_util import read_input_file

ELF = '#'
SPACE = '.'

#Directions
N = (-1, 0)
NE = (-1, 1)
NW = (-1, -1)
S = (1, 0)
SE = (1, 1)
SW = (1, -1)
E = (0, 1)
W = (0, -1)

# Direction groupings
DIRS = (N, NE, NW, S, SE, SW, E, W)
DIRGROUPING = {N: (N, NE, NW), S: (S, SE, SW), E: (NE, E, SE), W: (NW, W, SW)}
NEXTDIR = {N: S, S: W, W: E, E: N}


def parse_lines():
    lines = read_input_file(23)
    
    elves = deque()
    for r in range(len(lines)):
        l = lines[r]
        for c in range(len(l)):
            if l[c] == ELF:
                elves.append((r, c))
            
    return elves

def build_grid(elves:list):
    minR, maxR = float('inf'), float('-inf')
    minC, maxC = float('inf'), float('-inf')
    for r, c in elves:
        minR, maxR = min(minR, r), max(maxR, r)
        minC, maxC = min(minC, c), max(maxC, c)
    
    grid = []
    spaces = 0 
    for r in range(minR, maxR+1):
        row = []
        for c in range(minC, maxC+1):
            if (r, c) in set(elves):
                row.append(ELF)
            else:
                row.append(SPACE)
                spaces += 1
        grid.append(row)
    return grid, spaces



def print_grid(grid):
    s = ''
    for row in grid:
        s += ''.join(row) + '\n'
    print(s)
    return s
                


# 8 positions adjacent
# If elf in any adjacent, then do nothing
def check_adjacent(elf:tuple, uelves:set):
    r, c = elf
    for dr, dc in DIRS:
        if (r+dr, c+dc) in uelves:
            return True
    return False


# Check 3 positions in direction
# If an elf is in any, then return false
def check_side(elf:tuple, uelves:set, dir:str):
    r, c = elf
    for dr, dc in DIRGROUPING[dir]:
         if (r+dr, c+dc) in uelves:
            return False
    return True


def run_round(elves:list, dir:str):
    uelves = set(elves)
    proposed = [] # track each elve's proposed location
    proposedcounts = defaultdict(int) # keep count of each proposed location
    
    # Proposal Step
    for i, e in enumerate(elves):
        d = dir
        # check adjacent if there are any elves, if no elves, do nothing
        if check_adjacent(e, uelves):
            found = False
            # Check each directional grouping until a side with no elves is found
            for _ in range(4):
                if check_side(e, uelves, d):
                    found = True
                    break
                d = NEXTDIR[d]
            
            if found:
                # Propose move in direction
                p = (e[0]+d[0], e[1]+d[1])
                proposed.append(p)
                proposedcounts[p] += 1
            else:
                proposed.append(None)
        else:
            proposed.append(None)
            
    # If no elf needs to move, then we can break early
    if len(proposedcounts) == 0:
        return elves, None

    # Move Step
    for i, p in enumerate(proposed):
        # Either no proposed or more than 1 elf proposed
        if p is None or proposedcounts[p] != 1:
            continue
        # Move elf
        elves[i] = p
            
    return elves, NEXTDIR[dir]



def solution1():
    elves = parse_lines()
    dir = N
    
    rounds = 10
    while rounds > 0:
        elves, dir = run_round(elves, dir)
        
        if dir is None:
            break
        rounds -= 1
    
    grid, spaces = build_grid(elves)
    print_grid(grid)
    return spaces
    
    
    
def solution2():
    elves = parse_lines()
    dir = N
    
    rounds = 0
    while True:
        elves, dir = run_round(elves, dir)
        rounds += 1
        if dir is None:
            break
        
    
    grid, spaces = build_grid(elves)
    print_grid(grid)
    return rounds
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
