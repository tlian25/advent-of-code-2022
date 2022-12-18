# Day 18. Boiling Boulders
# https://adventofcode.com/2022/day/18

from collections import deque
from util.input_util import read_input_file


def parse_lines():
    lines = read_input_file(18)
    cubes = []
    for l in lines:
        # (x, y, z) location of cube
        cubes.append(tuple([int(x) for x in l.split(',')]))
        
    return set(cubes)
    

def get_sides(cubes):
    sides = []
    for x, y, z in cubes:
        # check all 6 sides
        for d in (-1, 1):
            if (x+d, y, z) not in cubes:
                sides.append((x+d, y, z))
            if (x, y+d, z) not in cubes:
                sides.append((x, y+d, z))
            if (x, y, z+d) not in cubes:
                sides.append((x, y, z+d))
                
    return sides

def solution1():
    cubes = parse_lines()
    sides = get_sides(cubes)
    return len(sides) 


def get_limits(cubes):
    # Get maxes. Mins known to be 0
    mx, my, mz = 0, 0, 0
    for x, y, z in cubes:
        mx = max(mx, x)
        my = max(my, y)
        mz = max(mz, z)
    return mx+1, my+1 , mz+1


def build_outer_shell(cubes, X, Y, Z):
    shell = set()
    #BFS
    q = deque([(0, 0, 0)])
    while q:
        x, y, z = q.popleft()
        if (x, y, z) in shell:
            continue
        
        shell.add((x, y, z))
        # Look in all 6 directions and look one box beyond the outer boundaries
        for d in (-1, 1):
            if -1 <= x+d < X+1 and (x+d, y, z) not in shell and (x+d, y, z) not in cubes:
                q.append((x+d, y, z))
            if -1 <= y+d < Y+1 and (x, y+d, z) not in shell and (x, y+d, z) not in cubes:
                q.append((x, y+d, z))
            if -1 <= z+d < Z+1 and (x, y, z+d) not in shell and (x, y, z+d) not in cubes:
                q.append((x, y, z+d))
                
    return shell
        

    
def solution2():
    cubes = parse_lines()
    X, Y, Z = get_limits(cubes)
    
    shell = build_outer_shell(cubes, X, Y, Z)
    sides = get_sides(shell)
    # Filter out sides that are on the outer part of the shell.
    # Only count a side if there's a lava cube on the other side.
    count = 0
    for x, y, z in sides:
        if (x, y, z) in cubes:
            count += 1
    
    return count
    
    
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
