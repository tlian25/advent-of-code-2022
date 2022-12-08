# Day 8. Treetop Tree House 
# https://adventofcode.com/2022/day/8

from util.input_util import read_input_file

def build_matrix():
    lines = read_input_file(8)
    matrix = []
    for l in lines:
        matrix.append([int(x) for x in l])
    return matrix

# Globals - Ugly and not OOP, but whatever.
matrix = build_matrix()
NROW = len(matrix)
NCOL = len(matrix[0])


def traverse_vertical(col, down=True) -> set:
    start = 0 if down else len(matrix)-1
    end = len(matrix) if down else -1
    step = 1 if down else -1
    visible = set()
    
    max_height = -1
    for r in range(start, end, step):
        h = matrix[r][col]
        if h > max_height:
            visible.add((r, col))
            max_height = h

    return visible
    
    
def traverse_horizontal(row, right=True) -> set:
    start = 0 if right else NCOL-1
    end = NCOL if right else -1
    step = 1 if right else -1
    visible = set() # Outer edge always visible
    
    max_height = -1
    for c in range(start, end, step):
        h = matrix[row][c]
        if h > max_height:
            visible.add((row, c))
            max_height = h

    return visible


def solution1():
    visible = set()
    # From top and bottom
    for col in range(NCOL):
        visible.update(traverse_vertical(col, True))
        visible.update(traverse_vertical(col, False))
        
    # From left and right
    for row in range(NROW):
        visible.update(traverse_horizontal(row, True))
        visible.update(traverse_horizontal(row, False))
    
    return len(visible)


def search_in_direction(r:int, c:int, step:tuple) -> int:
    a = step[0]
    b = step[1]
    h = matrix[r][c]
    
    r += a
    c += b
    
    view = 0
    while 0 <= r < NROW and 0 <= c < NCOL:
        view += 1
        if matrix[r][c] < h:
            r += a
            c += b
        else:
            break
    
    return view
            
        
    
    
def prod(l:list):
    p = 1
    for x in l:
        p *= x
    return p

    
def solution2():
    # 4 direction search
    matrix = build_matrix()
    NROW = len(matrix)
    NCOL = len(matrix[0])
    
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    
    maxv = 0
    for r in range(0, NROW):
        for c in range(0, NCOL):
            v = []
            for d in dirs:
                v.append(search_in_direction(r, c, d))
            
            maxv = max(maxv, prod(v))
            
    return maxv    
            
                
    
    
        
        
        
    
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
