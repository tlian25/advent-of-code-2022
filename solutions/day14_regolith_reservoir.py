# Day 14. Regolith Reservoir
# https://adventofcode.com/2022/day/14

from util.input_util import read_input_file

# Constants
ROCK = '#'
AIR = '.'
SAND = 'o'
ABYSS = 'A'
START = (0, 500)

def parse_coords(s) -> tuple:
    a, b = s.split(',')
    return int(a), int(b)

def parse_lines():
    lines = read_input_file(14)
    # split at -> to draw lines between points
    minCOL, maxCOL = float('inf'), 0
    maxROW = 0
    filled_spaces = set() # set of (x, y)
    # create grid later since we don't know total dimensions
    for l in lines:
        s = l.split(' -> ')
        for i in range(1, len(s)):
            src = parse_coords(s[i-1])
            dst = parse_coords(s[i])
            # always draw to right and to down
            if src > dst:
                src, dst = dst, src
            
            # Draw line from src to dst
            a, b = int(src[0]), int(src[1])
            c, d = int(dst[0]), int(dst[1])
            # either vertical line or horizontal line
            if a == c: #vertical line
                #print('vertical', src, dst)
                for row in range(b, d+1):
                    filled_spaces.add( (row, a) )
            elif b == d: # horizontal line
                #print('horizontal', src, dst)
                for col in range(a, c+1):
                    filled_spaces.add( (b, col) )
            else:
                raise ValueError(f"Diagonals not handled: {src}, {dst}")
            
            # Update max/mins
            maxCOL = max(maxCOL, a, c)
            minCOL = min(minCOL, a, c)
            maxROW = max(maxROW, b, d)
            
            
    print("Limits:", minCOL, maxCOL, maxROW)
            
    return filled_spaces, minCOL, maxCOL, maxROW


def create_grid(filled_spaces:set, minCOL:int, maxCOL:int, maxROW:int):

    grid = [[AIR for c in range(minCOL-1, maxCOL+2)] for r in range(0, maxROW+1)] 
    grid.append([ABYSS for X in range(len(grid[0]))])
    
    for r, c in filled_spaces:
        c -= minCOL-1
        grid[r][c] = ROCK
    
    return grid
    
    
    
# Return True if reached ABYSS
def drop_sands(grid, minCOL) -> bool:
    NCOLS = len(grid[0])
    r = START[0]
    c = START[1] - minCOL + 1
    count = 0
    while True:
        # Straight down
        if grid[r][c] == ABYSS:
            return count
        
        elif grid[r+1][c] not in (ROCK, SAND):
            r += 1

        # Else look down-left
        elif 0 <= c-1 and grid[r+1][c-1] not in (ROCK, SAND):
            r += 1
            c -= 1
        
        # Else look down-right
        elif c+1 < NCOLS and grid[r+1][c+1] not in (ROCK, SAND):
            r += 1
            c += 1
        
        # Else place sand and reset at top
        else: # Blocked and need to start at top again
            # modification for part 2 - if SAND is start, then we end
            grid[r][c] = SAND
            count += 1
            if r == START[0] and c == START[1] - minCOL + 1:
                return count
 
            r = START[0]
            c = START[1] - minCOL + 1
            

        



# Sand pouring in from (500, 0)
# produced one unit at a time
# Always falls down one if possible, else down-left, else down right
# else next unit of sand created at start

def solution1():
    filled_spaces, minCOL, maxCOL, maxROW = parse_lines()
    grid = create_grid(filled_spaces, minCOL, maxCOL, maxROW)
    
    #for g in grid:
    #    print(''.join(g))
    
    count = drop_sands(grid, minCOL)
    
    #print('\n FILLED GRID \n')
    #for g in grid:
    #    print(''.join(g))
    return count
        
    

    
def solution2():
    filled_spaces, minCOL, maxCOL, maxROW = parse_lines()
    # modify floor - replace ABYSS row with full rocks
    maxROW += 1 # We already append abyss row at end
    # Need to expand grid as sand could pile up and spread out
    minCOL -= maxROW * 2
    maxCOL += maxROW * 2
    grid = create_grid(filled_spaces, minCOL, maxCOL, maxROW)
    grid[-1] = [ROCK for _ in range(len(grid[0]))]
    
    count = drop_sands(grid, minCOL)
    
    return count
    
    
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
