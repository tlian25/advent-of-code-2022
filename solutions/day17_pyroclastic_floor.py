# Day 17. Pyroclastic Flow 
# https://adventofcode.com/2022/day/17

from util.input_util import read_input_file

ROCK = '#'
AIR = '.'
WIDTH = 7
# Each rock start left edge is 2 units away from left wall
# bottom edge is 3 units above highest rock or floor
# push in direction of gas
# falling one unit down

from collections import deque

class Rock:
    def __init__(self):
        self.rock = deque()
        self.L = 2
        self.R = 0
        
    def add_row(self, row:str):
        l = len(row)
        self.R = max(self.R, 2 + l - 1)
        row = deque([AIR, AIR] + list(row) + [AIR for _ in range(WIDTH-l-2)])
        self.rock.appendleft(row)
        
    def init(self, offset:int = 0):
        self.rock_coord = []
        # Get top and bot edges
        for c in range(WIDTH):
            for r in range(len(self.rock)):
                if self.rock[r][c] == ROCK:
                    self.rock_coord.append((r+offset, c))

    def check_left(self, grid):
        for r, c in self.rock_coord:
            if c-1 < 0 or (r, c-1) in grid:
                return False
        return True
    
    def check_right(self, grid):
        for r, c in self.rock_coord:
            if c+1 >= WIDTH or (r, c+1) in grid:
                return False
        return True
    
    def check_down(self, grid):
        for r, c in self.rock_coord:
            if r-1 < 0 or (r-1, c) in grid:
                return False
        return True

    def push_left(self):
        for i in range(len(self.rock_coord)):
            r, c = self.rock_coord[i]
            self.rock_coord[i] = (r, c-1)
    
    def push_right(self):
        for i in range(len(self.rock_coord)):
            r, c = self.rock_coord[i]
            self.rock_coord[i] = (r, c+1)

    def push_down(self):
        for i in range(len(self.rock_coord)):
            r, c = self.rock_coord[i]
            self.rock_coord[i] = (r-1, c)
            
    def push(self, s, grid):
        if s == '>':
            if self.check_right(grid):
                self.push_right()
        elif s == '<':
            if self.check_left(grid):
                self.push_left()
        else:
            raise ValueError(f"Unknown direction: {s}")


class Jet:
    def __init__(self, pattern):
        self.pattern = pattern
        self.mod = len(self.pattern)
        self.curr = -1
    
    def next(self):
        self.curr = (self.curr + 1) % self.mod
        return self.pattern[self.curr], self.curr
        

def parse_lines():
    lines = read_input_file(17)
    pattern = lines[0]
    
    rocks = []
    r = Rock()
    for l in lines[2:]:
        if l == '':
            rocks.append(r)
            r = Rock()
        else:
            r.add_row(l)
    rocks.append(r)
    
    return rocks, pattern
        

def print_grid(grid):
    maxh = 0
    minh = float('inf')
    for r, c in grid:
        maxh = max(maxh, r)
        minh = min(minh, r)
    
    s = ''
    for r in range(maxh, minh-1, -1):
        for c in range(7):
            if (r, c) in grid:
                s += ROCK
            else:
                s += AIR
        s += '\n'
    print(s)
        

        
def solution1(N = 2022):
    rocks, pattern = parse_lines()
    rock_mod = len(rocks)
    jet = Jet(pattern)

    grid = set()
    bottom_offset = 0
    
    count = 0
    curridx = 0

    while count < 1937:
        # Drop rock
        count += 1

        rock = rocks[curridx]
        rock.init(bottom_offset + 3)
        
        AtRest = False
        while not AtRest:
            dir, jetidx = jet.next()
            rock.push(dir, grid)
            
            if rock.check_down(grid):
                rock.push_down()
            else:
                AtRest = True

        # Add rock to grid and find next bottom_offset
        
        if curridx == 0 and jetidx == 0:
            grid.clear()
        
        for r, c in rock.rock_coord:
            grid.add((r, c))
            bottom_offset = max(bottom_offset, r+1)
            
        curridx = (curridx + 1) % rock_mod

    return bottom_offset
        

def get_bottom_offset(grid, maxheight):
    minh = [20 for _ in range(WIDTH)]
    for r, c in grid:
        minh[c] = min(minh[c], maxheight -r)
    return tuple(minh)
    
    

    
def solution2():
    rocks, pattern = parse_lines()
    rock_mod = len(rocks)
    jet = Jet(pattern)

    grid = set()
    bottom_offset = 0
    count_at_seen = {} # to detect cycles
    height_at_count = {}
    
    count = 0
    curridx = 0

    N = 1_000_000_000_000
    while count < N:
        count += 1
        # Drop rock
        rock = rocks[curridx]
        rock.init(bottom_offset + 3)
        
        AtRest = False
        while not AtRest:
            dir, jetidx = jet.next()
            rock.push(dir, grid)
            
            if rock.check_down(grid):
                rock.push_down()
            else:
                AtRest = True

        for r, c in rock.rock_coord:
            grid.add((r, c))
            bottom_offset = max(bottom_offset, r+1)
            
        # Detect Cycles
        # If we saw this state of the world before, we break out of cycle.
        s = (curridx, jetidx, get_bottom_offset(grid, bottom_offset))
        if s in count_at_seen:
            c1 = count_at_seen[s]
            h1 = height_at_count[c1]
            print('Count at last seen:', c1)
            print('Height at last seen:', h1)
            
            c2 = count
            h2 = bottom_offset
            print('Count at current seen:', c2)
            print('Height at current seen:', h2)
            
            # Diffs
            cd = c2 - c1
            hd = h2 - h1
            print('Count diff:', cd)
            print('Heigh diff:', hd)
            break
            count_at_seen.clear()
        
        count_at_seen[s] = count
        height_at_count[count] = bottom_offset
        curridx = (curridx + 1) % rock_mod

    # Broke out of loop. Apply modulos to get height. Make adjustments for starting and ending.
    starting_height = h1
    ending_count = (N - c1) % cd
    ending_height = height_at_count[c1 + ending_count] - height_at_count[c1]
    middle_height = ((N - c1) // cd) * hd
    total = starting_height + middle_height + ending_height
    return total

    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
