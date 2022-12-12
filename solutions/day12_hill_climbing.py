# Day 
# https://adventofcode.com/2022/day/

from collections import deque
import heapq
from util.input_util import read_input_file

def elevation(c:str):
    return ord(c) - ord('a')


def parse_lines():
    lines = read_input_file(12)
    # a == lowest
    # z == highest
    # S == current position
    # E == best signal
    NROWS = len(lines)
    NCOLS = len(lines[0])
    
    START = None
    END = None
    
    grid = []
    for r in range(NROWS):
        row = []
        for c in range(NCOLS):
            e = lines[r][c]
            if e == 'S':
                START = (r, c)
                e = 'a'
            elif e == 'E':
                END = (r, c)
                e = 'z'
            row.append(elevation(e))
        grid.append(row)
        
    return grid, START, END

def dist(CURR, END):
    return ((CURR[0]-END[0]) ** 2 + (CURR[1]-END[1]) ** 2) ** 0.5
            

# BFS from START to END
def bfs(grid, START, END):
    NROWS = len(grid)
    NCOLS = len(grid[0])
    q = deque([(0, 0, START[0], START[1])])
    seen = set()
    DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while q:
        h, steps, r, c = q.popleft()
        if (r, c) == END:
            return steps
        
        if (r, c) in seen:
            continue
        
        seen.add((r, c))
        for x, y in DIRS:
            nextr = r + x
            nextc = c + y
            # Check in bounds
            if 0 <= nextr < NROWS and 0 <= nextc < NCOLS:
                if (nextr, nextc) not in seen:
                    nexth = grid[nextr][nextc]
                    if nexth <= h + 1:
                        q.append((nexth, steps+1, nextr, nextc))
                    

# Reverse BFS from END to first elevation a
def reverse_bfs(grid, END):
    NROWS = len(grid)
    NCOLS = len(grid[0])
    q = deque([(25, 0, END[0], END[1])])
    seen = set()
    DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while q:
        h, steps, r, c = q.popleft()
        if h == 0:
            return steps
        
        if (r, c) in seen:
            continue
        
        seen.add((r, c))
        for x, y in DIRS:
            nextr = r + x
            nextc = c + y
            # Check in bounds
            if 0 <= nextr < NROWS and 0 <= nextc < NCOLS:
                if (nextr, nextc) not in seen:
                    nexth = grid[nextr][nextc]
                    if nexth >= h-1:
                        q.append((nexth, steps+1, nextr, nextc))


def solution1():
    grid, START, END = parse_lines()
    steps = bfs(grid, START, END)
    return steps

    
    
def solution2():
    grid, START, END = parse_lines()
    steps = reverse_bfs(grid, END)
    return steps
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
