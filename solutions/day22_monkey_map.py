# Day 22. Monkey Map
# https://adventofcode.com/2022/day/22

from util.input_util import read_input_file

ROCK = '#'
SPACE = '.'
INVALID = '@'
END = 'X'

RIGHT = 'R'
LEFT = 'L'
UP = 'U'
DOWN = 'D'

DIRMAP = {RIGHT: (0, 1), LEFT: (0, -1), UP: (-1, 0), DOWN: (1, 0)}
# Currdir: {L: newdir, R: newdir}
TURNMAP = {RIGHT: {RIGHT: DOWN, LEFT: UP},
           LEFT: {RIGHT: UP, LEFT: DOWN},
           UP: {RIGHT: RIGHT, LEFT: LEFT},
           DOWN: {RIGHT: LEFT, LEFT: RIGHT}}

ARROWMAP = {LEFT: u"\u2190", UP: u"\u2191", RIGHT: u"\u2192", DOWN: u"\u2193"}


def parse_lines():
    # Number - # of tiles to move
    # Letter - turn 90degress R or L 
    lines = read_input_file(22)
    
    n = ''
    cmds = []
    for c in lines[-1]:
        if c in (RIGHT, LEFT):
            if n:
                cmds.append(int(n))
            cmds.append(c)
            n = ''
        else:
            n += c
    
    if n:
        cmds.append(int(n))
    
    MAXL = 0
    for l in lines[:-2]:
        MAXL = max(MAXL, len(l))
    
    grid = []
    for l in lines[:-2]:
        s = l.replace(' ', INVALID)
        s += INVALID * (MAXL-len(s))
        grid.append(list(s))
    
    return cmds, grid

    
def find_start(grid):
    for x in range(len(grid[0])):
        if grid[0][x] == SPACE:
            return (0, x)


def traverse(cmds, grid):
    mY = len(grid)
    mX = len(grid[0])

    y, x = find_start(grid)
    currdir = RIGHT
    grid[y][x] = ARROWMAP[currdir]

    for c in cmds:
        # Turns
        if c in (RIGHT, LEFT):
            currdir = TURNMAP[currdir][c]
            grid[y][x] = ARROWMAP[currdir]
            continue
        
        # Moves
        dy, dx = DIRMAP[currdir]
        while c > 0:
            # Find next available space on grid
            ny, nx = (y+dy) % mY, (x+dx) % mX
            while grid[ny][nx] == INVALID:
                ny, nx = (ny+dy) % mY, (nx+dx) % mX
            
            # If next is Rock, then stop and stay where we are
            if grid[ny][nx] == ROCK:
                break
            # If next is Space -> move to it
            else:
                y, x = ny, nx
                grid[y][x] = ARROWMAP[currdir]
                c -= 1
            
    # Return to 1-indexed
    grid[y][x] = END
    return y+1, x+1, currdir


def cube_to_grid(cube):
    grid = []
    for row in range(4):
        for r in range(50):
            gridrow = []
            for col in range(3):
                c = row * 3 + col + 1
                gridrow += cube[c][r]
            grid.append(gridrow)
    return grid


def grid_to_cube(grid):
    MX = len(grid[0])
    MY = len(grid)
    cube = {}
    
    y = 0
    n = 1
    while y < MY:
        x = 0
        while x < MX:
            g = []
            for yi in range(y, y+50):
                g.append(grid[yi][x:(x+50)])
        
            cube[n] = g
            n += 1
            x += 50
        y += 50
    return cube



def print_grid(grid):
    s = ''
    for g in grid:
        s += ''.join(g) + '\n'
    print(s)
    return s


def print_cube(cube):
    for i, g in cube.items():
        print(i)
        print_grid(g)
    

# The ugliest hardcoding based on my cube
def get_next_on_cube(c, y, x, dir):
    # return c, y, x, dir
    dy, dx = DIRMAP[dir]
    if y+dy == -1: # Move up over to next cube
        if c == 2: return 10, x, 0, RIGHT
        if c == 3: return 10, 49, x, UP
        if c == 5: return 2, 49, x, UP
        if c == 7: return 5, x, 0, RIGHT
        if c == 8: return 5, 49, x, UP
        if c == 10: return 7, 49, x, UP
        raise ValueError(f'{c} - {y} - {x} - {dir}')

    elif y+dy == 50: # Move down over to next cube
        if c == 2: return 5, 0, x, DOWN
        if c == 3: return 5, x, 49, LEFT
        if c == 5: return 8, 0, x, DOWN
        if c == 7: return 10, 0, x, DOWN
        if c == 8: return 10, x, 49, LEFT
        if c == 10: return 3, 0, x, DOWN
        raise ValueError(f'{c} - {y} - {x} - {dir}')
        
    elif x+dx == -1: # Move left over to next cube
        if c == 2: return 7, 49-y, 0, RIGHT
        if c == 3: return 2, y, 49, LEFT
        if c == 5: return 7, 0, y, DOWN
        if c == 7: return 2, 49-y, 0, RIGHT
        if c == 8: return 7, y, 49, LEFT
        if c == 10: return 2, 0, y, DOWN
        raise ValueError(f'{c} - {y} - {x} - {dir}')
    
    elif x+dx == 50: # Move right over to next cube
        if c == 2: return 3, y, 0, RIGHT
        if c == 3: return 8, 49-y, 49, LEFT
        if c == 5: return 3, 49, y, UP
        if c == 7: return 8, y, 0, RIGHT
        if c == 8: return 3, 49-y, 49, LEFT
        if c == 10: return 8, 49, y, UP
        raise ValueError(f'{c} - {y} - {x} - {dir}')
    
    return c, y+dy, x+dx, dir
    

def traverse_cube(cmds, cube):
   
    c = 2
    y, x = find_start(cube[c])
    d = RIGHT
    cube[c][y][x] = ARROWMAP[d]
    
    for cmd in cmds:
        # Turns
        if cmd in (RIGHT, LEFT):
            d = TURNMAP[d][cmd]
            cube[c][y][x] = ARROWMAP[d]
            continue
        
        while cmd > 0:
            nc, ny, nx, nd = get_next_on_cube(c, y, x, d)
            # Find Next
            if cube[nc][ny][nx] == ROCK:
                break
            
            c, y, x, d = nc, ny, nx, nd
            cube[c][y][x] = ARROWMAP[d]
            cmd -= 1
                
    # Return to 1-indexed
    cube[c][y][x] = END
    return y+1, x+1, d




def find_end(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == END:
                # Return 1 indexed
                return y+1, x+1
            

def score(row, col, dir):
    if dir == RIGHT:
        d = 0
    elif dir == DOWN:
        d = 1
    elif dir == LEFT:
        d = 2
    elif dir == UP:
        d = 3
    return 1000 * row + 4 * col + d


def solution1():
    cmds, grid = parse_lines()
    y, x, d = traverse(cmds, grid)
    
    #print_grid(grid)    
    return score(y, x, d)

    
def solution2():
    cmds, grid = parse_lines()
    cube = grid_to_cube(grid)    
    y, x, d = traverse_cube(cmds, cube)
    grid = cube_to_grid(cube)
    
    #print_grid(grid)
    y, x = find_end(grid)
    return score(y, x, d)

    
    
 
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
